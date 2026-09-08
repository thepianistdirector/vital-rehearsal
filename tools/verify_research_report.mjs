// Optional development-only browser probe. Node and Chromium are not CLI dependencies.
// Uses an already available Chromium over pipes: no debugging/server port is opened.
import { spawn } from 'node:child_process';
import { access, mkdir, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const [reportPath, evidencePath] = process.argv.slice(2);
const executable = process.env.VITAL_REHEARSAL_BROWSER;
if (!reportPath || !evidencePath || !executable) {
  throw new Error('Usage: VITAL_REHEARSAL_BROWSER=/path/to/chromium node tools/verify_report.mjs report.html project-evidence-directory');
}
const output = resolve(evidencePath);
await mkdir(output, { recursive: true });
const profile = resolve('.cache', `report-browser-${Date.now()}`);
await mkdir(profile, { recursive: true });
const child = spawn(executable, [
  '--headless', '--remote-debugging-pipe', `--user-data-dir=${profile}`,
  '--disable-background-networking', '--disable-component-update', '--no-first-run',
  '--disable-sync', '--disable-default-apps', '--disable-extensions',
  '--disable-dev-shm-usage', 'about:blank',
], { stdio: ['ignore', 'ignore', 'pipe', 'pipe', 'pipe'] });
let sequence = 0;
let pending = new Map();
let buffer = Buffer.alloc(0);
let stderr = '';
const requests = [];
child.stderr.on('data', data => { stderr = (stderr + data.toString()).slice(-8000); });
child.on('exit', code => {
  for (const task of pending.values()) task.reject(new Error(`Chromium exited (${code}): ${stderr}`));
  pending.clear();
});
child.stdio[4].on('data', chunk => {
  buffer = Buffer.concat([buffer, chunk]);
  for (;;) {
    const boundary = buffer.indexOf(0);
    if (boundary < 0) break;
    const raw = buffer.subarray(0, boundary).toString();
    buffer = buffer.subarray(boundary + 1);
    if (!raw) continue;
    const message = JSON.parse(raw);
    if (message.method === 'Network.requestWillBeSent') requests.push(message.params.request.url);
    const task = pending.get(message.id);
    if (task) {
      pending.delete(message.id);
      message.error ? task.reject(new Error(JSON.stringify(message.error))) : task.resolve(message.result);
    }
  }
});
function send(method, params = {}, sessionId) {
  const id = ++sequence;
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => { pending.delete(id); reject(new Error(`CDP timeout: ${method}`)); }, 8000);
    pending.set(id, {
      resolve: value => { clearTimeout(timer); resolve(value); },
      reject: error => { clearTimeout(timer); reject(error); },
    });
    child.stdio[3].write(JSON.stringify({ id, method, params, ...(sessionId ? { sessionId } : {}) }) + '\0');
  });
}
try {
  const version = await send('Browser.getVersion');
  const { targetId } = await send('Target.createTarget', { url: 'about:blank' });
  const { sessionId } = await send('Target.attachToTarget', { targetId, flatten: true });
  const call = (method, params) => send(method, params, sessionId);
  const evaluate = async expression => {
    const response = await call('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true });
    if (response.exceptionDetails) throw new Error(JSON.stringify(response.exceptionDetails));
    return response.result.value;
  };
  await call('Page.enable');
  await call('Network.enable');
  await call('Network.setBlockedURLs', { urls: ['http://*', 'https://*', 'ws://*', 'wss://*'] });
  await call('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 1, mobile: false });
  await call('Page.navigate', { url: pathToFileURL(resolve(reportPath)).href });
  await evaluate('new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))');
  const layout = await evaluate(`({width: innerWidth, documentWidth: document.documentElement.scrollWidth,
    title: document.title, text: document.body.innerText,
    links: [...document.querySelectorAll('a')].map(a => a.getAttribute('href'))})`);
  if (layout.documentWidth > layout.width) {
    const failure = await call('Page.captureScreenshot', {format:'png',captureBeyondViewport:true});
    await writeFile(resolve(output,'report-phone-failed.png'),Buffer.from(failure.data,'base64'));
    await writeFile(resolve(output,'failure.json'),JSON.stringify(layout,null,2));
    throw new Error('Phone layout overflows the document');
  }
  if (!layout.text.includes('qualified') && !layout.text.includes('Qualified')) throw new Error('Scope limitation missing');
  const phone = await call('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true });
  await writeFile(resolve(output, 'report-phone.png'), Buffer.from(phone.data, 'base64'));
  const matched = await call('Page.captureScreenshot', {
    format: 'png', captureBeyondViewport: true,
    clip: { x: 0, y: 0, width: 390, height: 1500, scale: 1 },
  });
  await writeFile(resolve(output, 'report-phone-matched.png'), Buffer.from(matched.data, 'base64'));
  await call('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Tab', code: 'Tab', windowsVirtualKeyCode: 9 });
  await call('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Tab', code: 'Tab', windowsVirtualKeyCode: 9 });
  const focused = await evaluate('({text:document.activeElement.textContent,outline:getComputedStyle(document.activeElement).outlineStyle})');
  if (focused.text !== 'Skip to evidence' || focused.outline === 'none') throw new Error('Keyboard skip link/focus unavailable');
  await call('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Enter', code: 'Enter', windowsVirtualKeyCode: 13 });
  await call('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Enter', code: 'Enter', windowsVirtualKeyCode: 13 });
  const skipped = await evaluate('location.hash');
  if (skipped !== '#evidence') throw new Error('Skip link failed');
  for (const link of layout.links.filter(link => !link.startsWith('#'))) {
    if (!/^[A-Za-z_-]+\.(json|csv|pyz|txt)$/u.test(link)) throw new Error('Unexpected evidence link target');
    await access(resolve(dirname(reportPath), link));
  }
  const detailsBefore = await evaluate('[...document.querySelectorAll("details")].map(d=>d.open)');
  await evaluate('document.querySelector("summary").focus()');
  await call('Input.dispatchKeyEvent', {type:'keyDown',key:'Enter',code:'Enter',windowsVirtualKeyCode:13});
  await call('Input.dispatchKeyEvent', {type:'char',text:'\r',unmodifiedText:'\r',key:'Enter',windowsVirtualKeyCode:13});
  await call('Input.dispatchKeyEvent', {type:'keyUp',key:'Enter',code:'Enter',windowsVirtualKeyCode:13});
  await evaluate('new Promise(resolve=>requestAnimationFrame(resolve))');
  const detailsOpened = await evaluate('document.querySelector("details").open');
  if (!detailsOpened || detailsBefore.some(Boolean)) {console.log(await evaluate('({active:document.activeElement.outerHTML,states:[...document.querySelectorAll("details")].map(d=>d.open)})'));throw new Error('Keyboard result disclosure failed');}
  await call('Input.dispatchKeyEvent', {type:'keyDown',key:'Enter',code:'Enter',windowsVirtualKeyCode:13});
  await call('Input.dispatchKeyEvent', {type:'char',text:'\r',unmodifiedText:'\r',key:'Enter',windowsVirtualKeyCode:13});
  await call('Input.dispatchKeyEvent', {type:'keyUp',key:'Enter',code:'Enter',windowsVirtualKeyCode:13});
  const tableScroll = await evaluate(`(()=>{const d=document.querySelector('.scroll');if(!d)return null;d.focus();const before=d.scrollLeft;d.scrollLeft=100;return {before,after:d.scrollLeft,overflow:d.scrollWidth>d.clientWidth}})()`);
  if (tableScroll && tableScroll.overflow && tableScroll.after<=tableScroll.before) throw new Error('Narrow comparison table cannot scroll');
  await evaluate('if(document.querySelector(".scroll"))document.querySelector(".scroll").scrollLeft=0;document.activeElement.blur()');
  const semantics = await evaluate(`({language:document.documentElement.lang,
    mains:document.querySelectorAll('main').length,
    headerScopes:[...document.querySelectorAll('th')].map(th=>th.scope),
    statusText:[...document.querySelectorAll('.state strong')].map(x=>x.textContent),
    animations:document.getAnimations().length})`);
  if (semantics.language !== 'en' || semantics.mains !== 1 || semantics.headerScopes.some(x=>!['col','row'].includes(x))) {
    throw new Error('Report language/landmark/table semantics missing');
  }
  await call('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-reduced-motion', value: 'reduce' }] });
  if (semantics.animations !== 0) throw new Error('Unexpected report animation');
  await call('Emulation.setDeviceMetricsOverride', { width: 320, height: 844, deviceScaleFactor: 1, mobile: false });
  const reflow = await evaluate('({width:innerWidth,documentWidth:document.documentElement.scrollWidth})');
  if (reflow.documentWidth > reflow.width) throw new Error('320px layout overflows the document');
  await call('Emulation.setDeviceMetricsOverride', { width: 1280, height: 900, deviceScaleFactor: 1, mobile: false });
  await evaluate('scrollTo(0,0)');
  const desktop = await call('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true });
  await writeFile(resolve(output, 'report-desktop.png'), Buffer.from(desktop.data, 'base64'));
  await evaluate('document.documentElement.style.zoom = "200%"');
  const zoom = await evaluate('({width:innerWidth,documentWidth:document.documentElement.scrollWidth})');
  if (zoom.documentWidth > zoom.width) throw new Error('200% zoom overflows the document');
  if (requests.some(url => /^https?:/u.test(url))) throw new Error('Report requested an external resource');
  await writeFile(resolve(output, 'browser-check.json'), JSON.stringify({
    version, scope: 'automated report checks; not human accessibility or domain review',
    phone: { width: layout.width, documentWidth: layout.documentWidth }, keyboard: { focused, skipped }, zoom, reflow,
    semantics, detailsOpenedByKeyboard: detailsOpened, tableScroll, links: layout.links, evidenceLinkFilesExist: true, externalRequests: 0,
    remaining: ['manual assistive-technology use', 'human research workflow', 'qualified model review'],
  }, null, 2) + '\n');
  console.log('PASS: phone/320px reflow, keyboard skip/focus, 200% CSS zoom, offline evidence links, text states, no motion/external requests');
} finally {
  try { await send('Browser.close'); } catch {}
  if (child.exitCode === null) child.kill('SIGTERM');
}
