# PRIORITY DIRECTIVE — DESIGN QUALITY REBOOT (2026-11-18)
The user REJECTED the entire former design collection: 20 posters, both demo sites, coffee/cosmetics mockups, and mixed collages. **ZERO accepted projects. Do not reuse or publish them.**

For EVERY new work, first name **one concrete deliverable**: BUSINESS CARD, COFFEE PACK FRONT, COSMETIC TUBE, MARKETPLACE CARD, BROCHURE SPREAD, PRESENTATION SLIDE, WORKING WEB PAGE, AD POSTER, etc. A generic poster or collage is NOT a substitute. Show the actual physical/digital item by itself, clearly and legibly; supporting props must not take over.

**The central previous error was STYLE MONOCULTURE:** repeated dark backgrounds, similar serif/sans headlines, same aligned-left layouts, similar warm rim lighting, product-on-stone mockups and vast empty zones. The series MUST show contrasting design languages, not just change the subject matter. Mandatory **style divergence check**: for each new case, select different values across at least 4 of 7 axes: type family, palette, grid/layout, composition geometry, material/photography, illustration/graphic method, emotional tone. Audit the collection together. No single visual formula in more than 2 of any 10 consecutive independent cases.

Food-category truth: coffee must look delicious, warm, freshly brewed, natural and recognizably coffee-colored (espresso, roasted brown, crema, caramel, milk, warm paper). NO fantasy purple liquid, exploding coffee rings or unappetizing theatrics unless a specific commissioned brief explicitly calls for it.

Follow the **mandatory 48-check rubric** in PORTFOLIO_QUALITY_STANDARD.md and the variation matrix in PORTFOLIO_PRODUCTION_PLAN.md. Hard fail for any critical defect, any criterion below 5/5, uncertain brand data, typographic errors, poor device/print usability, insufficient diversity, or empty non-product render. Mark FAIL/UNVERIFIED, not PASS, where evidence is lacking. Every rejected artifact goes to drafts, not published gallery; only user-approved, verified cases may ship.

No public mention of AI tools. Do not invent real brands' logos, SKUs, product specifications or commissioned status. Default to distinctive imaginary smaller brands when genuine reference assets are absent.

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
