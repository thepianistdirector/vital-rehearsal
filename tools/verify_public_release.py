#!/usr/bin/env python3
"""Anonymous public release retrieval, integrity check and safe extraction."""
from pathlib import Path
from urllib.request import Request,urlopen
import datetime,hashlib,json,tarfile,time
ROOT=Path(__file__).resolve().parents[1];cache=ROOT/'.cache/public-release-downloads';cache.mkdir(exist_ok=False)
receipt={'started_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'authentication':'No Authorization header or GitHub credential supplied; public HTTPS URLs','downloads':[]}
api='https://api.github.com/repos/thepianistdirector/vital-rehearsal/releases/tags/v1.0.0rc4'
with urlopen(Request(api,headers={'User-Agent':'Vital-Rehearsal-public-verification'}),timeout=30) as r:release=json.load(r)
assert not release['draft'] and release['prerelease'] and release['tag_name']=='v1.0.0rc4'
receipt.update(release_id=release['id'],release_url=release['html_url'],tag=release['tag_name'],published_at=release['published_at'])
expected=json.loads((ROOT/'dist/RELEASE_INVENTORY.json').read_text());byname={x['filename']:x for x in expected['artifacts']}
for a in release['assets']:
 name=a['name'];assert Path(name).name==name
 target=cache/name;started=time.monotonic();digest=hashlib.sha256();size=0
 with urlopen(Request(a['browser_download_url'],headers={'User-Agent':'Vital-Rehearsal-public-verification'}),timeout=60) as r,target.open('xb') as f:
  status=r.status
  while chunk:=r.read(1024*1024):f.write(chunk);digest.update(chunk);size+=len(chunk)
 actual=digest.hexdigest();assert size==a['size'];assert a['digest']=='sha256:'+actual
 if name in byname:assert actual==byname[name]['sha256'] and size==byname[name]['bytes']
 else:assert actual==hashlib.sha256((ROOT/'dist'/name).read_bytes()).hexdigest()
 receipt['downloads'].append({'name':name,'public_url':a['browser_download_url'],'http_status':status,'bytes':size,'sha256':actual,'seconds':time.monotonic()-started})
 (ROOT/'docs/publication/v1/public-download-verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(name,'VERIFIED',flush=True)
assert set(byname)<=set(a['name'] for a in release['assets'])
archive=cache/'vital-rehearsal-1.0.0rc4-linux-x86_64-py312.tar.gz';destination=ROOT/'.cache/public-download-check'
with tarfile.open(archive) as t:t.extractall(destination,filter='data')
package=destination/'vital-rehearsal-1.0.0rc4';manifest=json.loads((package/'PACKAGE-MANIFEST.json').read_text())
for name,digest in manifest['files'].items():assert hashlib.sha256((package/name).read_bytes()).hexdigest()==digest,name
receipt.update(status='PASS',extracted_files_verified=len(manifest['files']),package_path=str(package),scope='Anonymous public download and local same-host extraction; not external human reproduction')
(ROOT/'docs/publication/v1/public-download-verification.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({'status':'PASS','assets':len(receipt['downloads']),'package':str(package)},indent=2))
