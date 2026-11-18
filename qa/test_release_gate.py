import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
from check_release import inspect, GATES


class TestVisualReleaseGate(unittest.TestCase):
    def doc(self, root):
        (root/"index.html").write_text("test site",encoding="utf8")
        (root/"qa").mkdir(exist_ok=True)
        proof = root/"qa"/"proof.txt"
        proof.write_text("manual review marker",encoding="utf8")
        ph = hashlib.sha256(proof.read_bytes()).hexdigest()
        sha = hashlib.sha256((root/"index.html").read_bytes()).hexdigest()
        return {"candidate_version":"reviewed-v1","candidate_sha256":sha,"release_ready":True,
                "gates":{g:{"status":"PASS","reason":"reviewed",
                            "evidence":[{"file":"qa/proof.txt","sha256":ph}]} for g in GATES}}

    def test_valid_proof_format(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); self.assertEqual(inspect(self.doc(root),root,release=True),[])

    def test_any_fail_rejects(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); x=self.doc(root); x["gates"]["G03"]["status"]="FAIL"
            self.assertTrue(inspect(x,root,release=True))

    def test_unverified_rejects(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); x=self.doc(root); x["gates"]["G08"]["status"]="UNVERIFIED"
            self.assertTrue(inspect(x,root,release=True))

    def test_false_pass_no_proof_rejects(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); x=self.doc(root); x["gates"]["G04"]["evidence"]=[]
            self.assertTrue(inspect(x,root,release=True))

    def test_wrong_release_checksum_rejects(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); x=self.doc(root); x["candidate_sha256"]="0"*64
            self.assertTrue(inspect(x,root,release=True))

    def test_blocked_release_rejects(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); x=self.doc(root); x["release_ready"]=False
            self.assertTrue(inspect(x,root,release=True))

    def test_proof_traversal_rejects(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); x=self.doc(root); x["gates"]["G02"]["evidence"]=[
                {"file":"../../../etc/passwd","sha256":"0"*64}]
            self.assertTrue(inspect(x,root,release=True))


if __name__=="__main__": unittest.main()
