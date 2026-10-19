import json
from pathlib import Path
import tempfile
import unittest
from experiment import score, assemble, schedule, summarize

class ScoringTests(unittest.TestCase):
    def setUp(self):
        self.cases=[{'id':'a','category':'proposal','expected':{'owner':None,'deadline':None}}]
    def test_correct(self):
        self.assertEqual(score('[{"id":"a","owner":null,"deadline":null}]',self.cases)['passed'],1)
    def test_invented_owner(self):
        r=score('[{"id":"a","owner":"Lee","deadline":null}]',self.cases)
        self.assertEqual(r['passed'],0)
        self.assertEqual(r['cases'][0]['wrong_fields'],['owner'])
    def test_missing_extra_duplicate_and_fields(self):
        for output in ['[]','[{"id":"b","owner":null,"deadline":null}]',
                       '[{"id":"a","owner":null,"deadline":null},{"id":"a","owner":null,"deadline":null}]',
                       '[{"id":"a","owner":null,"deadline":null,"extra":1}]']:
            with self.subTest(output=output):
                self.assertFalse(score(output,self.cases)['schema_valid'])
                self.assertFalse(score(output,self.cases)['exact'])
    def test_invalid_json_types_and_wrappers(self):
        for output in ['```json\n[]\n```','null','{}','[1]','[{"id":"a","owner":false,"deadline":null}]','NaN']:
            with self.subTest(output=output):
                self.assertEqual(score(output,self.cases)['passed'],0)
    def test_duplicate_keys_and_impossible_dates(self):
        for text in ['[{"id":"a","owner":null,"owner":"Lee","deadline":null}]',
                     '[{"id":"a","owner":null,"deadline":"2027-02-30"}]']:
            self.assertFalse(score(text,self.cases)['schema_valid'])
    def test_order_is_part_of_contract(self):
        cases=self.cases+[{'id':'b','category':'proposal','expected':{'owner':None,'deadline':None}}]
        self.assertFalse(score('[{"id":"b","owner":null,"deadline":null},{"id":"a","owner":null,"deadline":null}]',cases)['schema_valid'])
    def test_whitespace_not_penalized(self):
        self.assertTrue(score(' \n[{"id":"a", "deadline":null, "owner":null}]\n',self.cases)['exact'])

class DesignTests(unittest.TestCase):
    def test_schedule_balances_positions(self):
        rows=schedule(3)
        self.assertEqual(len(rows),9)
        for arm in ['short','rules','examples']:
            self.assertEqual(sorted(i%3 for i,x in enumerate(rows) if x['arm']==arm),[0,1,2])
    def test_assembly_does_not_leak_targets(self):
        c=[{'id':'x','note':'visible note','expected':{'owner':'SECRET'},'rationale':'SECRET'}]
        text=assemble('instructions',c)
        self.assertIn('visible note',text)
        self.assertNotIn('SECRET',text)
    def test_summary_counts_failed_runs_as_zero(self):
        rows=[{'arm':'short','repeat':1,'status':'timeout','elapsed_seconds':1}]
        out=summarize(rows,Path('/unused'),[{'id':'a','category':'proposal','expected':{'owner':None,'deadline':None}}])
        self.assertEqual(out['arms']['short']['passed'],0)
        self.assertEqual(out['arms']['short']['total'],1)
        self.assertEqual(out['arms']['short']['execution_failures'],1)


class RunnerTests(unittest.TestCase):
    def test_complete_runner_with_simulated_transport(self):
        from unittest.mock import patch
        from types import SimpleNamespace
        import subprocess
        import experiment
        with tempfile.TemporaryDirectory() as directory:
            target=Path(directory)/'run'
            call_count=0
            def transport(command, **kwargs):
                nonlocal call_count
                call_count+=1
                if call_count==1:
                    raise subprocess.TimeoutExpired(command,1,output=b'partial',stderr=b'timed out')
                if call_count==2:
                    return SimpleNamespace(returncode=2,stdout='',stderr='simulated failure')
                output=Path(command[command.index('--output-last-message')+1])
                cases=json.loads((experiment.ROOT/'dataset.json').read_text())
                output.write_text(json.dumps([{'id':c['id'],**c['expected']} for c in cases if c['split']=='heldout']))
                return SimpleNamespace(returncode=0,stdout='simulated execution',stderr='')
            with patch('experiment.subprocess.check_output',return_value='test-runtime'),patch('experiment.subprocess.run',side_effect=transport):
                self.assertEqual(experiment.run(target,1,'test-model',1),1)
            report=json.loads((target/'scores.json').read_text())
            self.assertEqual(report['arms']['short']['execution_failures'],1)
            self.assertEqual(report['arms']['rules']['execution_failures'],1)
            self.assertEqual(report['arms']['examples']['passed'],16)
            self.assertIn('partial',(target/'1-short.log.txt').read_text())
            self.assertTrue((target/'frozen/PROTOCOL.md').exists())
            with self.assertRaises(FileExistsError): experiment.run(target,1,'test-model',1)
    def test_invalid_bounds(self):
        import experiment
        with self.assertRaises(ValueError): experiment.schedule(0)
        with self.assertRaises(ValueError): experiment.run(Path('/unused'),0,'model',1)

class ReportingTests(unittest.TestCase):
    def test_paired_improvements_and_regressions(self):
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)
            cases=[{'id':'a','category':'one','expected':{'owner':'Lee','deadline':None}},
                   {'id':'b','category':'two','expected':{'owner':None,'deadline':None}}]
            for arm,owners in [('short',[None,None]),('rules',['Lee','Wrong']),('examples',['Lee',None])]:
                (p/f'1-{arm}.output.txt').write_text(json.dumps([{'id':c['id'],'owner':o,'deadline':None} for c,o in zip(cases,owners)]))
            rows=[{'trial':f'1-{a}','arm':a,'repeat':1,'status':0,'elapsed_seconds':1} for a in ['short','rules','examples']]
            r=summarize(rows,p,cases)
            self.assertEqual(r['paired_case_observations']['short_to_rules']['improved'],1)
            self.assertEqual(r['paired_case_observations']['short_to_rules']['regressed'],1)
            self.assertEqual(r['paired_case_observations']['rules_to_examples']['both_pass'],1)
    def test_empty_and_unpaired_reports(self):
        self.assertEqual(summarize([],Path('/unused'),[])['arms'],{})

if __name__=="__main__": unittest.main()
