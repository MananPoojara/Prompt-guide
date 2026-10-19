"""Simulated runtime faults; these are not observed model failures."""
import json,subprocess,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import run
class RuntimeTests(unittest.TestCase):
    def invoke(self,out,*flags):
        with patch.object(sys,'argv',['run','--output',str(out),*flags]):run.main()
    def test_invalid_outputs_exhaust_budget_and_resume_does_not_call(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'run'
            with patch('run.subprocess.run',return_value=subprocess.CompletedProcess([],0,'','')) as model:
                self.invoke(out);self.assertEqual(model.call_count,6)
                self.invoke(out,'--resume');self.assertEqual(model.call_count,6)
            self.assertFalse(json.loads((out/'state.json').read_text())['done'])
    def test_timeout_consumes_call_and_stops(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'run'
            with patch('run.subprocess.run',side_effect=subprocess.TimeoutExpired('codex',180)) as model:
                self.invoke(out);self.assertEqual(model.call_count,1)
            s=json.loads((out/'state.json').read_text());self.assertEqual(s['calls'],1);self.assertEqual(s['history'][0]['status'],'timeout')
    def test_pending_call_requires_inspection(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'run'
            with patch('run.subprocess.run',side_effect=KeyboardInterrupt):
                with self.assertRaises(KeyboardInterrupt):self.invoke(out)
            with patch('run.subprocess.run') as model:
                with self.assertRaises(SystemExit):self.invoke(out,'--resume')
                model.assert_not_called()
if __name__=='__main__':unittest.main()
