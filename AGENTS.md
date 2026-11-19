# KAREV CREATIVE QUALITY RULE / v4.0 (top priority)

**Before any design, inspect [PORTFOLIO_QUALITY_STANDARD.md](PORTFOLIO_QUALITY_STANDARD.md). It is the current authoritative rubric, superseding v3's 48 checks.**

- **Individual artifact:** 100 explicitly weighted checks in 10 domains, total 100; applied hard gates by medium. Any applicable FAIL or critical UNVERIFIED is a REJECTION, regardless of weighted aggregate. Only 100/100 with evidence can be considered for user review.
- **Portfolio diversity:** a separate weighted 20-check/100-point gate. Compare actual thumbnails and finished artifacts, not prompts. Do not use one typeface/palette/composition/lighting recipe across unrelated works. Neighboring cases differ across 4 of 7 axes; no more than 2 cases out of 10 share the same formula.
- **Exact deliverables** come first: if the brief says tube, show a separate tube; if business card, provide front and back; if packaging, provide the actual package design and flat artwork. Never substitute generic posters, grids, collages, marketing scenes.
- **Food appeal/category:** coffee must look warm, natural, desirable to drink, and coffee-toned. Avoid surreal splashes as a substitute for design.
- **No fabricated real logos, products, claims, client relationships or references.** Public assets and portfolio copy have no mention of AI tools. Independent concepts must be clearly labeled, not misrepresented as commissioned.
- All previous design collections were rejected by the user: **0 accepted**. No rejected item may be promoted on the live website. Only user-reviewed and explicitly user-approved projects may be published.
- The weighted scores are diagnostic, not permission to trade a serious fault for strengths elsewhere. Scores require inspected outputs and records, not confident predictions.

## Non-negotiable portfolio quality rule: 5/5 ONLY

**Every portfolio project, image, presentation, visual, graphic or interactive experience must reach a genuine 5/5 before it may be called ready, proposed for publication or added to the gallery. A 4/5 is a FAIL, not an acceptable compromise.** Volume, deadlines and the number of generated variants never lower this standard.

Read and apply [PORTFOLIO_QUALITY_STANDARD.md](PORTFOLIO_QUALITY_STANDARD.md) for every new creative project. Rate the final exported artifact (not just its prompt or mockup) on concept/originality, composition and typography, brand/product fidelity, execution and details, and commercial usability. **All five dimensions must score 5/5**; a single dimension at 4/5 or lower blocks release. Averages and rounded scores are prohibited.

When any dimension is below 5/5: **REJECT -> record concrete defects -> rework or restart -> inspect the new export**. Never silently promote a mediocre result to pass; do not accumulate weak filler to satisfy a quota. Do not publish before the user's review and approval.

Public portfolio pages and creative assets must NOT mention AI, neural networks or generation tools. For real companies, use their authentic logos and verifiable products; clearly mark unsolicited brand work as an independent concept, never imply it was commissioned.

This is stricter than earlier diagnostic thresholds (including W01–W10). Earlier checks remain required but cannot override the 5/5 quality gate.

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

## Mandatory WOW art-direction gate for the whole website

Before reporting an art-directed portfolio site or creative design as ready, also read and apply the shared skill `karevholytek-hub/ai-shared-knowledge/.agents/skills/wow-art-direction-gate/SKILL.md`.

- First-screen screenshot on desktop and mobile must present a striking, intentional artistic scene, not a gradient/card template.
- Iconography must be a consistent author-designed set; no arbitrary emojis or anonymous rectangles masquerading as complete graphic elements.
- Show differentiated, substantial project previews, not empty placeholders. Label speculative work clearly.
- For the requested Luminescence direction: actual luminous flora, atmosphere, volumetric light and dandelion seeds drifting with wind. Do not insert literal mushrooms or cats into the no-cat Luminescence concept.
- Evaluate W01–W10 in addition to G01–G08. Any score < 3, or a weak hero, means REJECTED; green CI does not equal artistic quality.
- Keep the original GitHub Pages design unchanged while the user assesses separate creative candidates.
