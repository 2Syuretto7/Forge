# Acceptance criteria (EXECUTION_PLAN.md Section 12)

Status of each criterion on the working branch, with how it was checked.

| # | Criterion | Status | Evidence |
| --- | --- | --- | --- |
| 1 | The deployed site opens with no console errors | Deployed | The `deploy` workflow publishes to https://2syuretto7.github.io/Forge/ (deployment reported success). The build it publishes loads the map and every lesson with no console errors when served locally (`npm run e2e`, `npm run e2e:path`); the live page itself could not be opened from the build environment, whose network policy blocks github.io. |
| 2 | The map shows 24 nodes and every edge, with three edge styles and toggles | Met | The map (`#/map`, one click from the dashboard) draws 24 nodes and 61 edges (45 prerequisite, 7 cross-track, 9 long-range, as in `content/graph.yaml`); each toggle hides exactly its own style. |
| 3 | All 24 lessons complete per the validator | Met | `npm run validate` checks all 24 lessons with no phase list: hours, theory share, exercises, gradient checks, directives, edges, annotations, notebooks. |
| 4 | Every exercise's solution passes and starter fails; every notebook runs in `SMALL=1` | Met | CI runs `npm run pytest` (307 exercises in CPython), `npm run pyodide-test` (the same in Pyodide) and `npm run notebooks` (all 15 notebooks). |
| 5 | Every GPU notebook opens in Colab and prints a code the app accepts | Met, T4 check by the owner | The repository is public and every notebook is reachable at the URL its button opens. `npm run e2e:path` enters each notebook's full-run completion code and the app accepts all 15. `docs/colab-check.md` lists the codes and what was verified without a GPU. |
| 6 | Feynman grading works with a key and degrades without one | Met without a key; with a key needs the owner's | Without a key the lesson offers the rubric self-assessment and never blocks progress (`npm run e2e:path` completes every Feynman block that way). The request shape, the JSON parsing, the single retry and the error display are unit-tested against a mocked API. |
| 7 | Completing a lesson schedules reviews that appear in `#/review` and the next recall bridge | Met | `tests/e2e/phase2.spec.ts`. |
| 8 | Retro-annotations appear in earlier lessons after later ones are complete | Met | `tests/e2e/phase2.spec.ts`. |
| 9 | Progress survives reload; export and import round-trip exactly | Met | `tests/e2e/smoke.spec.ts`. |
| 10 | Lighthouse accessibility at least 90 on map and lesson; usable at 380 px | Met | Lighthouse 12.6: accessibility 100 and best practices 100 on the dashboard, the map, lesson pages and the exercise workspace. At 380 px wide no screen (every movement of every lesson, the map, reviews, settings) has content past the right edge. |
