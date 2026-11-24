import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from check_change_scope import is_public_visual


class ScopeTests(unittest.TestCase):
    def test_public_html_requires_release(self):
        self.assertTrue(is_public_visual("index.html"))
        self.assertTrue(is_public_visual("demo.html"))
    def test_site_assets_require_release(self):
        for x in ("assets/cat.webp","css/site.css","js/cat-rig.js","images/demo.png","public/bg.avif"):
            self.assertTrue(is_public_visual(x),x)
    def test_isolated_marketplace_has_separate_qa(self):
        for x in ("marketplace/index.html","marketplace/catalog.json","marketplace/media/choker/01.webp"):
            self.assertFalse(is_public_visual(x),x)
        for x in ("index.html","assets/marketplace.webp","demo.html"):
            self.assertTrue(is_public_visual(x),x)
    def test_docs_and_qa_do_not_trigger_release(self):
        for x in ("AGENTS.md","QA_PLAN.md","qa/release.json","qa/test_release_gate.py",
                  ".github/workflows/visual-quality.yml","docs/notes.html","qa/proof.png"):
            self.assertFalse(is_public_visual(x),x)


if __name__=="__main__":
    unittest.main()
