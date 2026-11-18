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


## Mandatory workflow for each intermediate work package

When the user asks to continue a complex multi-step project, first check the active unfinished task in `QA_PLAN.md` and the latest QA evidence. Do NOT treat the task as cancelled merely because a previous chat response ended.

**Before coding, image generation, redesign, or a new subtask, state in the user-facing conversation:**
1. The **intermediate goal**: exactly what observable user-facing outcome this step is supposed to deliver.
2. The **detailed execution plan**: inputs/reference photos, required changes, implementation order, risk controls, and tests.
3. **Acceptance and rejection criteria**: which concrete failures block this step.

**Then execute during the active turn:** inspect actual files, make the change, run reproducible tests, inspect real frames or recordings, and deliver the created artifact or a precise blocker. After the work, report what passed, failed, was not verified, and remains outstanding. A green automated test does not prove visual quality.

If starting another independent step, write its goal/plan/criteria **before** working on it. Never claim progress between user turns or in the background unless a real scheduled automation is running. Never say "done" for unfinished or unverified work. Do not publish partial builds to `main` without G01–G08 PASS.
