# SHALLOWS / CONCEPT 03 — REVIEW ONLY
Date: 2026-11-18
Status: CANDIDATE — user review needed. **DO NOT MERGE / DO NOT PUBLISH.**

## Art direction
Sunlit clear shallow water, sand caustics, slow refractive echo, sparse bubbles emerging from seabed points and wobbling upward, restrained ivory/teal typography, six authored cohesive translucent-material SVG icons. No dark abyss, stock UI icons, or sea clichés (shells/anchors).

## Contents
- `concept-03.html`: self-contained page (embedded original hero image/WebP; no third-party image or font fetch)
- `index.html`: existing Luminescence unchanged except the small 01/03 concept switcher
- 6 authored pictogram illustrations, 3 explicitly marked independent design studies: AURA/MODUL/NOMA
- Mobile navigation; pause/resume for bubbles and photographic light echo; reduced-motion fallback

## Checks performed locally (Chromium rendering of the actual candidate HTML via set_content)
- 1440×900 / 768×1024 / 390×844: no horizontal overflow (`scrollWidth == clientWidth`)
- 390px: mobile menu opens, closes on section selection, state updates
- 390px: motion button pauses and resumes, state updates
- 1440px & 390px: canvas frame image hashes differ when playing, remain identical while paused, differ again after resuming
- reduced-motion: paused by default
- no pageerror exceptions observed in test

## Visual risk / outstanding release checks
- Subjective W01–W10 art approval pending from user; never self-certify 5/5.
- No test on physical Android Chrome or iOS Safari. Mobile screenshots are Chromium viewport simulations, not device approval.
- Animation FPS/real-device GPU performance not measured. Do not promise 60 FPS.
- No true business projects or external contacts supplied; 3 cards labelled "Авторский концепт", and no invented email/Telegram link.
- QA G01/G04/G05 partially checked technically; real-user G06/G08 remain UNVERIFIED, other project-specific cat motion gates in `qa/release.json` are unrelated and unchanged.
- GitHub Pages delivery untested; candidate intentionally not merged to main.
- Inspect actual full-page visual before any merge; good-looking screenshot alone is not final approval.

## Acceptance rule
Visual quality standard 5/5 on every axis from PORTFOLIO_QUALITY_STANDARD.md, W01 and W02 at 4/4, all other W criteria >= 3, total >=32/40 and G01–G08 applicable gates PASSED. **Fail any critical criterion => reject and rebuild; don't publish.**
