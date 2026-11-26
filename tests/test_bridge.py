import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import bridge as b

class TestBridge(unittest.TestCase):
    def test_gemini_success(self):
        raw=json.dumps({'event':'result','result':{'status':'SUCCESS','response':'OK'}})
        self.assertEqual(b.parse('gemini',raw),'OK')
    def test_gemini_error(self):
        with self.assertRaises(ValueError):b.parse('gemini','{"event":"result","result":{"status":"ERROR","response":"fake"}}')
    def test_gemini_missing_or_duplicate(self):
        for raw in ['','{"event":"init"}', '\n'.join(['{"event":"result","result":{"status":"SUCCESS","response":"ok"}}']*2)]:
            with self.assertRaises(ValueError):b.parse('gemini',raw)
    def test_claude_success(self):
        self.assertEqual(b.parse('claude','{"subtype":"success","is_error":false,"result":"ok"}'),'ok')
    def test_claude_failure(self):
        for raw in ['{}','{"subtype":"error","result":"ok"}','{"subtype":"success","is_error":true,"result":"ok"}']:
            with self.assertRaises(ValueError):b.parse('claude',raw)
    def test_request_pins_model(self):
        with patch.object(b,'exe',return_value='agy'):
            cmd,body=b.request('gemini','x','gemini-4-carbon-high')
            self.assertIn('gemini-4-carbon-high',cmd);self.assertNotIn('-p',cmd);self.assertTrue(json.loads(body)['message']['content'].endswith('x'))
    def test_bad_model(self):
        with self.assertRaises(ValueError):b.model_name('claude','opus & whoami')
    def test_verdict(self):
        h='a'*64
        self.assertTrue(b.verdict(f'VERDICT: AGREE\nREVIEWED_SHA256: {h}\nNo objection.',h))
        self.assertFalse(b.verdict(f'VERDICT: REJECT\nREVIEWED_SHA256: {h}\nObjection.',h))
        self.assertFalse(b.verdict(f'VERDICT: AGREE\nREVIEWED_SHA256: {h}\nNo objection.', 'b'*64))
    def test_audit(self):
        with tempfile.TemporaryDirectory() as d:
            p,q,bib=[Path(d)/x for x in ['old.tex','new.tex','ok.bib']]
            p.write_text('% AW-LOCK-BEGIN thm\nA\n% AW-LOCK-END thm\n\\label{x}\n')
            q.write_text(p.read_text()+'\\cite{good}\n');bib.write_text('@article{good,\n title={Example}\n}')
            self.assertEqual(b.audit(p,q,[bib]),[])
            q.write_text(q.read_text().replace('\nA\n','\nB\n')+'\\cite{fake}')
            self.assertEqual(len(b.audit(p,q,[bib])),2)
    def test_failed_cli_no_response(self):
        with tempfile.TemporaryDirectory() as d,patch.object(b,'exe',return_value='claude'),patch.object(b.subprocess,'run',return_value=SimpleNamespace(returncode=1,stdout='bad',stderr='error')):
            out=Path(d)/'x.txt'
            with self.assertRaises(RuntimeError):b.run('claude','prompt',out)
            self.assertFalse(out.exists());self.assertEqual(json.loads(Path(str(out)+'.meta.json').read_text())['status'],'FAILED')
    def test_signoff_records_and_mutation(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);candidate=root/'paper.tex';candidate.write_text('Original claim.\n');h=b.sha(candidate)
            reply=f'VERDICT: AGREE\nREVIEWED_SHA256: {h}\nNo objection.'
            prompt=candidate.read_text()+'\n'+h
            with patch.object(b,'agent_ready'),patch.object(b,'exe',return_value='fake'):
                for provider,raw in [('gemini',json.dumps({'event':'result','result':{'status':'SUCCESS','response':reply}})),('claude',json.dumps({'subtype':'success','result':reply}))]:
                    with patch.object(b.subprocess,'run',return_value=SimpleNamespace(returncode=0,stdout=raw,stderr='')):
                        b.run(provider,prompt,root/provider)
            codex=root/'codex';codex.write_text(reply)
            self.assertTrue(b.verify(candidate,codex,root/'gemini',root/'claude'))
            candidate.write_text('Changed claim.\n');self.assertFalse(b.verify(candidate,codex,root/'gemini',root/'claude'))

if __name__=='__main__':unittest.main()
