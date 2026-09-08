"""Research contract and actual worker regression checks (same-host software evidence)."""
import csv
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from vital_rehearsal.research import example,validate,sha,canonical_json,MODEL,run,inspect
from vital_rehearsal.contracts import ContractError
ROOT=Path(__file__).resolve().parents[1]

def sealed(model=MODEL,**changes):
    obj=example(model);obj.update(changes);obj['seal']=sha(canonical_json(obj));return obj

class Research(unittest.TestCase):
    def setUp(self):
        (ROOT/'.cache').mkdir(exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(dir=ROOT/'.cache');self.root=Path(self.temp.name)
    def tearDown(self):self.temp.cleanup()
    def test_seal_binds_settings(self):
        obj=sealed();obj['rtol']=1e-6
        with self.assertRaises(ContractError):validate(obj)
    def test_model_coupling_and_outside_domain_rejected(self):
        for changes in [{'model':'untrusted.py'},{'resistance_scale':1.2},{'time_unit':'minute'},{'samples':True},{'rtol':float('nan')},{'source_sha256':'0'*64},{'coupling':{'drug':'x'}}]:
            obj=example(MODEL);obj.update(changes)
            with self.assertRaises((ContractError,ValueError)):validate(obj,False)
    def test_scheduler_duplicate_and_boolean_rejected(self):
        for changes in [{'servers':True},{'jobs':[{'id':'x','arrival_s':0,'service_s':1}]*2},{'jobs':[{'id':'x','arrival_s':-1,'service_s':1}]}]:
            with self.assertRaises(ContractError):validate(sealed('synthetic-fcfs',**changes))
    def test_scheduler_known_two_server_schedule(self):
        spec=sealed('synthetic-fcfs',servers=2,jobs=[{'id':'a','arrival_s':0,'service_s':3},{'id':'b','arrival_s':0,'service_s':1},{'id':'c','arrival_s':0,'service_s':2},{'id':'d','arrival_s':4,'service_s':1}])
        directory,result=run(spec,self.root)
        self.assertEqual(result['execution_state'],'COMPLETED')
        rows=list(csv.DictReader((directory/'schedule.csv').read_text().splitlines()))
        self.assertEqual([(r['id'],float(r['start_s']),float(r['finish_s'])) for r in rows],[('a',0,3),('b',0,1),('c',1,3),('d',4,5)])
        self.assertEqual(inspect(directory)['metrics']['mean_wait_s'],.25)
    def test_actual_numerical_source_run_retains_semantic_warning(self):
        directory,result=run(sealed(duration_s=.1,samples=6),self.root)
        self.assertEqual(result['execution_state'],'COMPLETED')
        self.assertGreater(result['diagnostics']['source_derivative_max_abs_error_mmHg_per_s'],6)
        self.assertEqual(len(list(csv.DictReader((directory/'trajectory.csv').read_text().splitlines()))),6)
        self.assertEqual(inspect(directory)['conclusion'],'NUMERICAL_OUTPUT_WITH_SOURCE_WARNINGS')
        self.assertIn('NOT_ESTABLISHED',result['diagnostics']['physiological_validity'])
    def test_timeout_kept_and_new_attempt_preserves_previous(self):
        first,result=run(sealed(timeout_s=.01),self.root)
        self.assertEqual(result['execution_state'],'TIMED_OUT')
        firstbytes=(first/'manifest.json').read_bytes()
        second,result=run(sealed('synthetic-fcfs'),self.root)
        self.assertNotEqual(first,second);self.assertEqual(firstbytes,(first/'manifest.json').read_bytes())
        self.assertEqual(inspect(first)['execution_state'],'TIMED_OUT')
    def test_manifest_rejects_modified_or_added_artifacts(self):
        directory,result=run(sealed('synthetic-fcfs'),self.root)
        (directory/'schedule.csv').write_text('changed')
        with self.assertRaises(ContractError):inspect(directory)
    def test_original_archive_reruns_after_source_package_is_not_on_path(self):
        directory,result=run(sealed('synthetic-fcfs'),self.root)
        p=subprocess.run([sys.executable,'-I',str(directory/'source.pyz'),'research','run',str(directory/'study.json'),'--output',str(self.root/'rerun')],capture_output=True,text=True,cwd=self.root)
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)
        other=Path(json.loads(p.stdout)['bundle'])
        self.assertEqual((directory/'schedule.csv').read_bytes(),(other/'schedule.csv').read_bytes())

if __name__=='__main__':unittest.main()
