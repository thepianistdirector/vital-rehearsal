#!/usr/bin/env python3
"""Prepare an offline local candidate directory; no network or publication."""
from pathlib import Path
import argparse,hashlib,json,shutil,sys,zipfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from vital_rehearsal import __version__

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('destination',type=Path);a=p.parse_args();dest=a.destination.resolve();dest.mkdir(parents=True,exist_ok=False)
 build=ROOT/'dist'/f'vital-rehearsal-{__version__}.pyz'
 shutil.copy2(build,dest/'vital-rehearsal.pyz')
 for name in ['LICENSE','README.md','CONTRIBUTING.md','requirements.txt','research-requirements.txt','vital-rehearsal']:
  shutil.copy2(ROOT/name,dest/name)
 for name in ['src','scenarios','research','plan','examples']:
  shutil.copytree(ROOT/name,dest/name,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
 for name in ['ARCHITECTURE.md','EXPERIMENTS.md','SOURCES.md','ROADMAP.md','TASKS.md','STATUS.md']:
  shutil.copy2(ROOT/name,dest/name)
 shutil.copytree(ROOT/'docs',dest/'docs',ignore=shutil.ignore_patterns('__pycache__'))
 (dest/'tools').mkdir()
 for name in ['package_cli.py','prepare_v1_release.py','verify_v1_package.py','render_plan.py','validate_plan.py','verify_research_report.mjs']:
  if (ROOT/'tools'/name).exists():shutil.copy2(ROOT/'tools'/name,dest/'tools'/name)
 shutil.copytree(ROOT/'tests',dest/'tests',ignore=shutil.ignore_patterns('__pycache__'))
 (dest/'dist').mkdir()
 shutil.copy2(build,dest/'dist'/build.name)
 shutil.copy2(ROOT/'dist/vital-rehearsal-1.0.0rc1-investigation.pyz',dest/'dist/vital-rehearsal-1.0.0rc1-investigation.pyz')
 shutil.copytree(ROOT/'dist/wheels',dest/'wheels')
 lines=[];core=[]
 for f in sorted((dest/'wheels').glob('*.whl')):
  name,version=f.name.split('-')[:2];line=f'{name}=={version} --hash=sha256:{sha(f)}\n';lines.append(line)
  if name in ['numpy','scipy']:core.append(line)
 (dest/'requirements-lock.txt').write_text(''.join(core));(dest/'research-requirements-lock.txt').write_text(''.join(lines))
 notices=dest/'dependency-notices';notices.mkdir()
 for f in (dest/'wheels').glob('*.whl'):
  with zipfile.ZipFile(f) as z:
   for name in z.namelist():
    if 'dist-info' in name and any(n in name.lower() for n in ['license','copying','notice']) and not name.endswith('/'):
     target=notices/f.stem/Path(name).name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(z.read(name))
 (dest/'NOTICE.md').write_text('Application: AGPL-3.0; see LICENSE. The separately licensed Ben-Tal CellML and generated Python are CC BY 3.0, attributed in src/vital_rehearsal/BENTAL_NOTICE.txt. Dependency wheel notices are preserved in wheels/ and extracted in dependency-notices/. No article images or empirical patient data are distributed. Research includes original synthetic figures, source provenance and historical CLI paths (not credentials).\n')
 files={str(f.relative_to(dest)):sha(f) for f in sorted(dest.rglob('*')) if f.is_file()}
 (dest/'PACKAGE-MANIFEST.json').write_text(json.dumps({'version':__version__,'status':'LOCAL_CANDIDATE_NOT_PUBLIC','files':files},indent=2)+'\n')
 print(json.dumps({'directory':str(dest),'version':__version__,'files':len(files),'bytes':sum(f.stat().st_size for f in dest.rglob('*') if f.is_file()),'application_sha256':sha(dest/'vital-rehearsal.pyz')},indent=2))
if __name__=='__main__':main()
