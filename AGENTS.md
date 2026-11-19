# KAREV: поштучный отбор + Prompt Iteration Engine (действует с 19.11.2026)
**Прочитать перед любым новым дизайном:** [PORTFOLIO_QUALITY_STANDARD.md](PORTFOLIO_QUALITY_STANDARD.md) (версия 5.0); [skills/prompt-iteration-engine/SKILL.md](skills/prompt-iteration-engine/SKILL.md) (оригинальный навык из PR #9); [PORTFOLIO_ITERATION_WORKFLOW.md](PORTFOLIO_ITERATION_WORKFLOW.md).

- **Никаких оценок партии целиком с отбраковкой всех работ.** Оценивать каждое изделие отдельно. Даже 1–2 достойные работы из 20 — хороший результат.
- **Идею отделять от исполнения.** Диагностика по прежним 100 взвешенным критериям 0–5, идея 0–10, потенциал исправления 0–10. 90+ — сильный кандидат с возможностью точечных правок, 80–89 — перспективный, 70–79 — сохранить удачную идею, если она сильная, ниже 70 — возможен архив.
- **Никакого автоматического отказа при 99/100.** Любой правимый недостаток — конкретная задача итерации. Критические ошибки блокируют только *публикацию*, а не сохранение удачного замысла.
- Для нового промпта ОБЯЗАТЕЛЬНЫ четыре секции: BASELINE MUST (не менять), **LOCK/СОХРАНИТЬ** (удачные детали предыдущей версии), **FIX/ИСПРАВИТЬ** (причина, конкретные изменения, проверяемый результат), **AVOID/НЕ ПОВТОРЯТЬ** (замеченные ошибки + корректные альтернативы). Повторить QA и проверить регресс после правки. Сохранять BEST VERSION.
- После 2 повторений одного провала сменить **метод работы**, а не наращивать негативные указания. Для текста — точная вёрстка, для предметов — шаблон/маска/SVG/3D-основа.
- Один самостоятельный продукт за кадр: визитка отдельно, тюбик отдельно, пакет кофе отдельно. Подтверждённые фирменные знаки, свойства, размеры; публичные материалы без упоминания ИИ.
- Разнообразие — задача планирования и курирования, не проходной балл для всей партии. По пользователю без утверждения на сайт не публиковать.
- Зелёный тест не является художественной приёмкой. Применять старые G01–G08 / визуальные QA где подходят и не заявлять об отсутствии дефектов без проверки.

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
