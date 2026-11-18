# Obligatory visual QA for Karev portfolio

Every change to images, animation, design or site functionality MUST use the following review process BEFORE calling the work ready:

1. Read QA_PLAN.md and qa/release.json. Re-open the exact final build.
2. Apply photorealism-qa + visual-acceptance-gate from karevholytek-hub/ai-shared-knowledge/.agents/skills (main).
3. Independently check facial identity of Myshka against the user's original photographs; do not substitute generic ginger cats.
4. Check anatomy and all movement in a real-time browser recording, at natural speed. Changed pixel coordinates do not prove that the animal looks alive.
5. Run: python -m unittest discover -s qa -p "test_*.py"; python qa/check_release.py --mode lint; and python qa/browser_smoke.py --site . --out qa-artifacts.
6. Record G01–G08 as PASS, FAIL or UNVERIFIED with actual proof. Any FAIL or critical UNVERIFIED prevents release.
7. Never invent Telegram URLs, testimonials or real projects. Label design placeholders.
8. Do not merge a new animated cat to the live site until all gates pass and a release checksum is verified. If the user reports failure, immediately downgrade the affected gate to FAIL.
9. Report deficiencies and devices not tested; do not claim 60 FPS or Android verification from a desktop simulation.

Technical CI success alone does not establish artistic or behavioral quality. Every release needs visual human review.
