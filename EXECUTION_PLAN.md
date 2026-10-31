# Forge: Execution Plan for the AI Coding Agent

This file is the complete, self-contained specification for building **Forge**, a personal learning platform for the ML research and ML engineering skills expected at frontier AI labs. Read it fully before writing code. Execute the phases in order. Do not stop at a partial build: every phase ends with a working, deployed app, and the plan is finished only when every lesson passes the acceptance checks in Section 12.

**Math track (owner request, Phase 7).** The owner replaced the original four-lesson math track with a 38-lesson track, M01 to M38, specified in [`docs/math-track.md`](docs/math-track.md). That document is binding for the math track: its lessons, edges, lesson template, density minimums and gating rules. Where it and this file disagree, it wins for the math track, with one exception decided by the owner: progress is **reset** when the new curriculum first loads instead of being migrated (the API key, model and theme stay). The core lessons are numbered from L01, and progress saved under their earlier numbers is carried over (owner request).

---

## 0. Operating rules for the agent

1. **The owner does minimum manual work.** Never ask the owner to write code, content, tests, or configuration. Only ask for what cannot be automated: (a) creating the GitHub repository if you lack permission, (b) one Anthropic API key pasted into the app's Settings screen, (c) a free Google account for Colab. Everything else is yours.
2. **Never leave TODOs, placeholders, stubs, "lorem ipsum", or "content coming soon".** Every lesson you ship is complete: all movements, all exercises, all hidden tests, all reference solutions.
3. **Verify before you claim done.** Run `npm run check` (Section 11) after every task. A task is done only when it passes.
4. **Commit after each numbered task** with a message `phase-N/task-M: <summary>`.
5. **Default decisions are already made (Section 1).** Do not re-ask them. If the owner later changes one, update this file first, then the code.
6. **Mathematical and technical correctness outranks speed.** Every derivation step must be checked numerically in its exercise tests where possible. If unsure of a fact, derive it or test it; never invent citations, numbers, or paper results.
7. **Keep this file current.** Tick the checkboxes in Section 13 as you complete tasks.

---

## 1. Decisions and defaults

| Topic | Decision |
| --- | --- |
| Learner level | Assumes high-school calculus and basic Python. Math lessons start from first principles but move fast. |
| Pace | Slow and steady, enforced (docs/math-track.md, Pedagogy): a lesson unlocks when its prerequisites are complete and their Feynman blocks have passed; one lesson in progress at a time; due reviews come before a new movement; a lesson closes at 80% on its own review cards a week after completion. |
| Compute | Browser only (Pyodide + NumPy) for the 38 math lessons and 5 core lessons, browser plus Colab for 3 (L04, L09, L12), free Google Colab (T4 GPU) for 12. No paid compute required. |
| Target role | Balanced research engineer: ML theory + MLE systems equally weighted. |
| Hosting | Static site on GitHub Pages, deployed by GitHub Actions on every push to `main`. |
| Storage | Single learner. Progress in IndexedDB, with one-click JSON export/import in Settings. |
| AI grading | Anthropic Messages API called from the browser with the owner's key (stored only in the browser). Model ID configurable, default `claude-sonnet-5-5`. |
| Language | All UI and content in English. No emojis anywhere in UI or content. No stock images; all figures are generated SVG/canvas. |

---

## 2. Product summary

- **Positioning:** like Codecademy/DataCamp (browser lessons, runnable code beside text, instant checks, skill map, projects); unlike them (true prerequisite graph, 6 to 12 hour lessons, checks on numerics and gradients, derivations as first-class interactive content, a Feynman explanation step graded by AI).
- **Pedagogy:** the Feynman loop in every lesson: puzzle, derive, build from scratch, explain plainly, break it, reconnect.
- **50/50 rule:** in every lesson, theory minutes and practice minutes are each between 45% and 55% of the total. Enforced by the content validator.
- **Long-arc rule:** every lesson has 6 to 12 estimated hours, 6 to 8 movements, at least 12 exercises, and one capstone. Enforced by the validator.
- **Graph rule:** three edge types (vertical prerequisite, horizontal same-stage across tracks or math strands, long-range across stages). Every lesson has at least 1 inbound edge (except M01), at least 1 outbound edge (except L20), and at least 1 horizontal or long-range edge. Enforced by the validator.

---

## 3. Tech stack

| Layer | Choice | Notes |
| --- | --- | --- |
| Build | Vite 5+, TypeScript strict | `npm create vite@latest` with React-TS template |
| UI | React 18+, React Router (hash router for GitHub Pages) | No UI kit; small hand-written component set |
| Styling | CSS modules + CSS variables | Light and dark themes via `prefers-color-scheme` plus a toggle |
| Math | KaTeX | Rendered at build time where possible |
| Markdown | `unified` + `remark-parse` + `remark-math` + `remark-directive` + `rehype-katex` | Custom directives (Section 6) |
| Graph map | D3 (`d3-force`, `d3-zoom`) | Layered layout: x by track, y by stage, force for spacing |
| Interactive figures | Plain React + SVG/canvas components | One file per widget in `src/widgets/` |
| Python in browser | Pyodide (latest stable) in a Web Worker, with NumPy preloaded | Load lazily on first code pane |
| Code editor | CodeMirror 6 with Python mode | |
| Storage | `idb` wrapper over IndexedDB | Schema in Section 8 |
| AI grading | `fetch` to `https://api.anthropic.com/v1/messages` with header `anthropic-dangerous-direct-browser-access: true` | Key in IndexedDB only |
| Tests (app) | Vitest + Testing Library; Playwright for end-to-end | |
| Tests (content) | Python 3.11, pytest, NumPy, SymPy | Runs every exercise's reference solution against its hidden tests |
| Notebooks | Jupyter `.ipynb`, executed in CI with `papermill` in `SMALL=1` CPU mode | PyTorch CPU in CI; GPU on Colab |
| CI/CD | GitHub Actions: `check.yml` on PRs and pushes, `deploy.yml` to Pages on `main` | |

---

## 4. Repository layout

```
forge/
  EXECUTION_PLAN.md            this file
  README.md                    how to open the app; 5 lines max for the owner
  package.json
  vite.config.ts
  tsconfig.json
  .github/workflows/check.yml
  .github/workflows/deploy.yml
  content/
    graph.yaml                 tracks, stages, lessons, edges (single source of truth)
    lessons/
      L01/
        lesson.yaml            metadata, movements, edge markers, hooks
        m0-recall.md
        m1-puzzle.md
        m2-derivation.md
        ...                    one file per movement
        exercises/
          e01/
            prompt.md
            starter.py
            solution.py
            tests.py           hidden tests; pure NumPy; also run by pytest in CI
          ...
        capstone/
          prompt.md
          starter.py | notebook.ipynb
          solution.py
          tests.py
      L02/ ... L20/, M01/ ... M38/
    reviews/                   generated spaced-review items (built by script)
  notebooks/                   GPU lessons' Colab notebooks (copied from content at build)
  scripts/
    validate_content.ts        enforces all rules in Sections 2 and 6
    build_content.ts           compiles content/ into public/content/*.json
    run_exercise_tests.py      runs every solution against its tests
    run_notebooks.py           papermill SMALL=1 execution of every notebook
    gen_reviews.ts             builds spaced-review items from lesson metadata
  src/
    main.tsx
    app/                       routes, layout, theme
    graph/                     map view (D3)
    lesson/                    lesson player, movement renderer, edge markers
    code/                      CodeMirror pane, Pyodide worker, test runner
    widgets/                   interactive figures, one per file
    grader/                    Feynman grader client and rubric
    review/                    spaced-review engine (SM-2 variant)
    store/                     IndexedDB schema and hooks
    settings/                  API key, model ID, export/import, theme
  tests/
    unit/
    e2e/
```

---

## 5. App screens and behavior

### 5.0 Dashboard (home, route `#/`), added at the owner's request to bring the interface closer to Codecademy and DataCamp
- A "Resume" card that returns to the last lesson screen visited (or the next unfinished movement), with the lesson's step progress.
- Stats: XP earned, day streak, exercises solved, hours of the path completed; reviews due with a "Practice now" button.
- The syllabus by stage: one row per lesson with its status, track, hours, where it runs, a progress bar and Start, Continue, Review or Preview.
- XP: 100 per exercise, 30 less per hint taken (never below 25), 10 when finished with the solution; 10 per prediction (20 if right), 25 per movement, 250 per lesson, 50 per Feynman explanation, 300 per Colab capstone, 5 per graded review. The streak counts consecutive days with any activity.
- The top bar is shared by every screen: Learn, Map, Reviews (with the due count), Settings, the streak and the XP.

### 5.1 Map (route `#/map`; it was the home page before the dashboard)
- Full-screen graph. Columns = the six math strands (Number and information, Algebra and proof, Linear algebra, Calculus, Probability, Optimization), then 4 tracks (Core ML, Architectures, Systems (MLE), LLM science). Rows = 6 stages, numbered from 0 (Prelude, Foundations, Learning, Models + GPUs, Scale, Frontier); a math strand's lessons stack down its column.
- Node states: locked (prerequisites incomplete or their Feynman block not passed, still clickable for preview), available, in progress (ring shows percent), complete.
- Edges: vertical = solid gray arrow; horizontal = solid colored double arrow; long-range = dashed colored arrow. Toggle each type on/off.
- Hover a node: title, hours, theory/practice split, prerequisites, unlocks. Click: open lesson.
- Header shows: total hours done / total, reviews due today (click to start), Settings.
- Works on phone width (380px): map becomes a stage-by-stage list with edges listed as chips.

### 5.2 Lesson player (route `#/lesson/:id/:movement?`) and exercise workspace (route `#/lesson/:id/ex/:exercise`)
- A lesson bar under the top bar: a Syllabus drawer (movements with theory/practice tag, minutes and their exercises; the live theory/practice meter), the lesson title, and one progress segment per movement.
- Center: the movement content (markdown + math + widgets) in a reading column; each exercise is a step card with its status, XP and a Start, Continue or Review button. A sticky bottom bar holds Back, the count of tasks done, and Complete movement or Next.
- Exercises open in a full-screen workspace, as on DataCamp: instructions, hints (each costs XP) and the solution on the left; a dark editor with Run code and Submit answer, and a console with Output and Tests tabs, on the right; Previous, one dot per exercise of the movement, and Next exercise at the bottom. On a phone the three panels become tabs.
- Edge markers render inline as chips: "Reuses M27: KL divergence" (links back) and "Returns in L17" (links forward; disabled until reachable, shows a one-line teaser).
- Retro-annotations: when a later lesson is complete, its annotations appear as margin notes in earlier lessons.
- Gating (docs/math-track.md): a locked lesson, or any lesson while another is in progress, is a preview whose movements cannot be completed; a movement the learner has not opened yet shows the due review queue first and opens once it is cleared; after about 90 minutes of study a movement boundary suggests a break.
- Progress saves on every exercise pass, movement completion, and prediction submission.

### 5.3 Exercise runner
- Starter code loads into CodeMirror. "Run" executes user code in the Pyodide worker; "Check" runs hidden `tests.py` against it.
- Tests are Python functions `test_*`; the runner reports each pass/fail with message. Timeout 20 s per check; worker restarts on timeout.
- Hints: up to 3 per exercise, revealed one at a time; using hints is recorded but never blocks completion.
- "Show solution" unlocks after 3 failed checks, and marks the exercise "completed with solution" (counts for unlock, flagged for review).

### 5.4 Prediction blocks
- Learner commits a prediction (multiple choice, numeric, or sketch-on-axes) before a run or reveal. Stored, then compared after reveal with a short explanation. Score recorded as calibration data.

### 5.5 Feynman grader
- Text area (150 to 400 words). On submit, call the API with the rubric in Section 9. Show: score 0 to 4 per criterion, the specific gaps, and one follow-up question. Learner may revise and resubmit; best score kept.
- If no API key: show "Add your key in Settings to get feedback" and allow self-assessment against the rubric checklist instead. Never block progress.

### 5.6 GPU lessons
- Movement shows an "Open in Colab" button linking to `https://colab.research.google.com/github/<owner>/forge/blob/main/notebooks/<ID>.ipynb`.
- Each notebook ends with an autograder cell that runs tests and prints a completion code: `FORGE-<ID>-<8 hex chars>` where the hex is the first 8 chars of SHA-256 of `"<ID>:<sorted passed test names>:forge"`. The app verifies the code locally against the expected test list and marks the movement complete.

### 5.7 Reviews (route `#/review`)
- Daily queue from the spaced-review engine. Item types: re-derivation (fill in a derivation step), code kata (short exercise from an old lesson), concept check, prediction. SM-2 scheduling with grades 0 to 5.
- Due reviews also appear as each lesson's Movement 0 (recall bridge), filtered to the lessons with an edge into it (a horizontal edge counts both ways).
- One-week check: a completed lesson closes when, a week or more after completion, at least 80% of its review cards have been answered correctly; the dashboard shows each completed lesson's check.

### 5.8 Settings (route `#/settings`)
- API key (masked, stored locally, "Test key" button), model ID, theme, export progress JSON, import progress JSON, reset progress (with typed confirmation).

---

## 6. Content format

### 6.1 `content/graph.yaml`
```yaml
tracks: [math, core, arch, sys, llm]
stages: [prelude, foundations, learning, models_gpus, scale, frontier]
lessons:
  - id: L01
    title: Linear and logistic regression, end to end
    track: core
    stage: learning
    gpu: false
edges:
  - {from: M12, to: L01, type: vertical}
  - {from: L09, to: L07, type: horizontal, note: "Attention cost read on the roofline"}
  - {from: M27, to: L17, type: long_range, note: "KL divergence returns as the RLHF penalty"}
```
The full lesson and edge list is in Section 10; encode it exactly.

### 6.2 `lesson.yaml`
```yaml
id: L09
hours: 10
capstone: "Train a 2-layer transformer on character-level Shakespeare-style public-domain text to below 1.6 nats"
movements:
  - {file: m0-recall.md,     mode: theory,   minutes: 30}
  - {file: m1-puzzle.md,     mode: theory,   minutes: 45}
  - {file: m2-derivation.md, mode: theory,   minutes: 150}
  - {file: m3-build.md,      mode: practice, minutes: 150}
  - {file: m4-scale.md,      mode: practice, minutes: 60}
  - {file: m5-break.md,      mode: both,     minutes: 60}
  - {file: m6-feynman.md,    mode: theory,   minutes: 30}
  - {file: m7-capstone.md,   mode: practice, minutes: 75}
hooks:        # forward links shown at the end
  - {to: L08, text: "You will fuse this softmax into one kernel."}
reuses:       # backward links; drive Movement 0
  - {from: L03, concept: backprop through matrix products}
annotations:  # retro-annotations placed into earlier lessons when this lesson completes
  - {target: L01, anchor: softmax, text: "Softmax here is the same function that weights attention in L09."}
```
`mode: both` minutes count half to theory, half to practice.

### 6.3 Markdown directives
| Directive | Purpose | Required attributes |
| --- | --- | --- |
| `:::derivation` with `:::step` children | Step-through derivation; each step may have a blank to fill (`[[answer]]`) checked by SymPy-equivalent rule or numeric tolerance | `id` |
| `:::predict` | Commit-then-reveal prediction | `id`, `kind` (choice, numeric, sketch), `answer` |
| `:::exercise` | Embeds an exercise from `exercises/` | `ref` |
| `:::widget` | Embeds an interactive figure from `src/widgets/` | `name`, props as attributes |
| `:::edge` | Inline edge marker chip | `to` or `from`, `text` |
| `:::feynman` | Feynman explanation block | `id`, `prompt`, `key_points` (list for the rubric) |
| `:::colab` | Open-in-Colab button + completion-code box | `notebook` |
| `:::aside` | Optional depth note, collapsed by default | none |

### 6.4 Exercise contract
- `starter.py` defines function signatures with docstrings stating shapes and dtypes.
- `tests.py` imports the learner module as `sub` and defines `test_*` functions using only NumPy and the standard library. Required test kinds where applicable: value vs reference at tolerance, shape and dtype, gradient check by central finite differences (relative error < 1e-5 in float64), invariants (for example softmax rows sum to 1, attention is permutation-equivariant without positions), and edge cases.
- `solution.py` must pass all tests; CI enforces this.
- Each lesson: at least 12 exercises plus the capstone; at least 3 exercises include a gradient check where a gradient exists.

### 6.5 Validator (`scripts/validate_content.ts`) fails the build if any of these break
1. Every lesson in `graph.yaml` has a folder with `lesson.yaml` and all referenced files.
2. Edges reference existing lessons; vertical edges form a DAG; vertical edges never point from a later stage to an earlier stage.
3. Hours between 6 and 12; 6 to 8 movements; theory share between 45% and 55%.
4. At least 12 exercises and one capstone per lesson; every exercise has starter, solution, tests, prompt.
5. Each lesson has at least one `:::predict`, one `:::derivation`, one `:::feynman`, one `:::widget`, and one break-it movement.
6. Edge-count rules from Section 2; every `reuses` entry corresponds to a graph edge into the lesson; every `hooks` entry to an edge out of it.
7. No banned strings: `TODO`, `TBD`, `lorem`, `coming soon`, `placeholder`, and no emoji code points.
8. GPU lessons have a notebook with an autograder cell matching Section 5.6.
9. Math-track lessons (M01 to M38, docs/math-track.md): 10 or 12 hours in all eight movements at exactly 50% theory; 14 to 16 exercises plus the capstone; at least 3 exercises with a `test_grad*` check from M15 on and a `test_invariant*` check before M15; at least 5 predictions, 4 derivations, one widget in the puzzle or derivation and one in scale or break it; one plain-language Feynman block with 4 to 6 key points, plus a written proof (a Feynman block with id `proof*`, concept rubric) from Foundations on; edge chips to at least two lessons each way (fewer only when the graph has fewer); 8 to 12 review cards.
10. Every lesson folder under `content/lessons` is listed in `graph.yaml`.

---

## 7. Interactive widgets (build all; reused across lessons)

| Widget | Shows | Used in |
| --- | --- | --- |
| `MatrixTransform` | 2D linear map acting on a grid and unit circle; SVD axes overlay | M02, M07, M09 to M11, M13, M14, M18, M20, L16 |
| `DistributionPlayground` | Sample, fit by MLE, see likelihood surface | M22, M25, L02 |
| `ComputationGraph` | Forward values and backward gradients flowing on a graph | M19, L03, L04 |
| `EntropyBars` | Entropy, cross-entropy, KL between two editable distributions | M27, L17 |
| `DecisionBoundary` | Logistic regression boundary training live | L01 |
| `BiasVarianceCurve` | Train/test error vs capacity, double-descent regime | L02, L11 |
| `LossLandscape` | 2D loss surface with SGD/momentum/Adam trajectories | L05 |
| `ActivationStats` | Per-layer activation and gradient histograms under different inits and norms | L05, L06 |
| `Roofline` | Arithmetic intensity vs achievable FLOP/s; place kernels on it | L07, L08, L09, L18 |
| `AttentionHeatmap` | Q, K, V and attention weights for a toy sequence; causal mask toggle | L09, L19 |
| `TokenizerStepper` | BPE merges step by step | L10 |
| `ScalingFit` | Fit power laws to loss vs compute; compute-optimal frontier | L11 |
| `FloatFormats` | Bit layout and rounding of fp32, bf16, fp16, fp8 | L13, L18 |
| `ParallelismPlanner` | Memory per GPU for DP, ZeRO stages, TP, PP given model size | L14, L15 |
| `LossSpikeExplorer` | Replay a logged training run; inspect grad norm, LR, spikes | L15 |
| `KVCacheMeter` | KV cache memory vs batch, length, heads, precision | L18 |
| `RewardKLTradeoff` | Reward vs KL-to-reference as beta changes | L17 |
| `FeatureDictionary` | Sparse autoencoder features over toy activations | L19 |

All widgets: keyboard accessible, work at 380px width, light/dark themes, no external network calls.

---

## 8. Data model (IndexedDB, database `forge`, version 1)

| Store | Key | Fields |
| --- | --- | --- |
| `progress` | `lessonId` | `status`, `movementsDone[]`, `startedAt`, `completedAt`, `hoursLogged` |
| `exercises` | `lessonId/exerciseId` | `status` (unseen, attempted, passed, passed_with_solution), `attempts`, `hintsUsed`, `lastCode` |
| `predictions` | `lessonId/predictId` | `value`, `correct`, `at` |
| `feynman` | `lessonId/feynmanId` | `text`, `scores{}`, `gaps[]`, `bestTotal`, `at` |
| `reviews` | `itemId` | `ease`, `interval`, `due`, `reps`, `lapses`, `history[]` |
| `colab` | `lessonId` | `code`, `verifiedAt` |
| `settings` | `key` | `value` (apiKey, modelId, theme) |

Export/import writes and reads one JSON object with all stores and a `schemaVersion`.

---

## 9. Feynman grader specification

Request: `POST /v1/messages`, `max_tokens: 1200`, system prompt below, user content = lesson title, the prompt, the key points, and the learner's text. Require JSON output; parse defensively; on parse failure retry once, then show raw feedback.

System prompt (store in `src/grader/prompt.ts`):
```
You grade a learner's plain-language explanation of an ML concept, in the spirit of Richard Feynman: if they cannot explain it simply, they do not yet understand it.
Score 0-4 on each criterion:
- correctness: every claim is true; no hidden errors.
- completeness: covers each listed key point.
- plainness: no jargon left unexplained; a motivated 14-year-old could follow.
- mechanism: explains why it works, not just what it does.
- example: includes a concrete example or analogy that is accurate.
Return only JSON: {"scores":{"correctness":n,"completeness":n,"plainness":n,"mechanism":n,"example":n},"gaps":["..."],"follow_up":"one probing question"}
Be strict and specific. Quote the learner's phrase when pointing at an error. Never write the explanation for them.
```
Pass threshold for movement completion: total at least 14 of 20, or three submissions made (progress never blocks).

---

## 10. Curriculum

The math track is M01 to M38 in [`docs/math-track.md`](docs/math-track.md). The other tracks are L01 to L20 below; their edges from the math track are listed with them.

Every lesson follows the movement pattern in 6.2 (recall bridge, puzzle, derivation, build, scale/measure, break it, Feynman, capstone). Hours, content, edges and capstones below are binding. "Exercises" lists the minimum set; add more to reach at least 12 per lesson.

### Learning

**L01. Linear and logistic regression, end to end** (core, 8 h, browser)
- Derive: least squares from MLE under Gaussian noise; logistic regression from Bernoulli MLE; gradients of both; softmax regression; L2 as Gaussian prior.
- Build: closed-form and gradient-descent solvers, softmax classifier, feature standardization, evaluation metrics (accuracy, log loss, calibration curve).
- Break: unscaled features, perfectly separable data driving weights to infinity.
- Capstone: multi-class classifier on a provided tabular dataset reaching a stated accuracy, with calibration analysis.
- Edges in: M12, M25 (vertical); M30 (horizontal). Edges out: L02, L03 (vertical); L09 (long-range).

**L02. Generalization, bias-variance and double descent** (core, 7 h, browser)
- Derive: train/test split rationale, bias-variance decomposition for squared error, regularization, cross-validation, overparameterized interpolation and double descent with random features.
- Build: polynomial and random-feature regressions, k-fold CV, a double-descent curve.
- Break: test-set leakage; tuning on the test set.
- Capstone: reproduce a double-descent curve and explain where the peak sits.
- Edges in: L01, M25, M27 (vertical); M31 (horizontal). Edges out: L11 (vertical); L12 (long-range).

**L03. Neural networks and backprop from scratch** (core, 10 h, browser)
- Derive: MLP forward pass, universal approximation intuition, backprop as reverse-mode autodiff on matrix expressions, gradients for linear, ReLU, tanh, softmax-cross-entropy.
- Build: NumPy MLP with manual backward, gradient checks per layer, minibatch training on a provided spiral and digit-like dataset.
- Break: all-zero init symmetry; dead ReLUs; exploding activations from bad init.
- Capstone: 2-hidden-layer MLP reaching a stated accuracy, all gradients written by hand.
- Edges in: L01, M19 (vertical); M04 (long-range). Edges out: L04, L05, L09 (vertical); L17 (long-range).

**L04. Build a mini autograd engine; PyTorch internals** (sys, 10 h, browser + Colab)
- Derive: computation graphs, topological sort, tensor broadcasting rules and their gradients, memory saved for backward.
- Build: tensor autograd engine in NumPy (add, mul, matmul, sum, exp, log, relu, broadcasting, reshape), with an `nn.Module`-like API; train the L03 MLP on it. In Colab: compare against PyTorch, inspect `grad_fn`, write a custom `torch.autograd.Function`.
- Break: in-place ops corrupting saved tensors; broadcasting gradient bugs.
- Capstone: the engine trains an MLP to match the PyTorch reference loss curve within tolerance.
- Edges in: L03, M19 (vertical). Edges out: L07 (vertical); L05 (horizontal); L14 (long-range).

**L05. Optimization: SGD, momentum, Adam, schedules, initialization** (core, 9 h, browser)
- Derive: gradient descent on quadratics and condition number, momentum as a low-pass filter, RMSProp and Adam with bias correction, AdamW decoupled weight decay, warmup and cosine schedules, Xavier and He initialization from variance preservation.
- Build: each optimizer from scratch; schedule functions; init schemes; compare on the `LossLandscape` widget and on the L03 MLP.
- Break: learning rate too high; Adam without bias correction early in training; weight decay vs L2 inside Adam.
- Capstone: an optimizer bake-off report with a tuned recipe for the L03 task.
- Edges in: L03, M28 (vertical); L04, M29 (horizontal). Edges out: L06, L11 (vertical); L15 (long-range).

### Models and GPUs

**L06. Normalization, residuals and training stability** (arch, 8 h, browser)
- Derive: batch norm and layer norm forward and backward, RMSNorm, residual connections and gradient flow through depth, pre-norm vs post-norm.
- Build: each norm with manual backward and gradient checks; a 20-layer MLP with and without residuals and norms; activation statistics tracking.
- Break: post-norm deep stacks without warmup; batch norm with batch size 1.
- Capstone: train a 30-layer residual MLP stably and explain each stabilizing choice.
- Edges in: L05 (vertical); M34 (horizontal). Edges out: L09 (vertical); L08 (horizontal).

**L07. GPU architecture and the roofline model** (sys, 9 h, Colab)
- Derive: SMs, warps, memory hierarchy (registers, shared, L2, HBM), bandwidth vs compute bound, arithmetic intensity, roofline; FLOP counts for matmul and elementwise ops.
- Build: benchmark matmul and elementwise ops on the T4, place them on a measured roofline; profile with `torch.profiler`; measure the cost of host-device transfers.
- Break: tiny kernels dominated by launch overhead; unnecessary `.item()` syncs.
- Capstone: a profiling report that explains a provided slow training step and speeds it up by at least 2x.
- Edges in: L04 (vertical); M33 (horizontal). Edges out: L08, L13, L14 (vertical); L09 (horizontal).

**L08. Writing kernels: Triton, fused ops, FlashAttention** (sys, 11 h, Colab)
- Derive: tiling, memory coalescing, kernel fusion savings, online softmax (derive the running max and sum update), FlashAttention's IO complexity.
- Build: Triton vector add, fused softmax, tiled matmul, fused layer norm, a forward FlashAttention kernel tested against a reference.
- Break: numerically unstable softmax in fp16; wrong block sizes.
- Capstone: FlashAttention forward kernel matching reference within 1e-2 in fp16 and faster than the naive version at sequence length 2048.
- Edges in: L07, L09 (vertical); L06 (horizontal). Edges out: L18 (vertical).

**L09. Attention and the transformer from scratch** (arch, 11 h, browser + Colab)
- Derive: attention as soft lookup, scaled dot product (why divide by sqrt(d)), causal masking, multi-head attention, positional information (sinusoidal, RoPE), the full decoder block, parameter and FLOP counts.
- Build: NumPy attention with manual backward; permutation-equivariance tests; full decoder block in PyTorch in Colab.
- Break: missing scaling causing saturated softmax; mask off by one leaking the future.
- Capstone: train a 2-layer transformer on a provided public-domain character corpus to below a stated loss.
- Edges in: L03, L06 (vertical); L07, M34 (horizontal); L01, M07, M10 (long-range). Edges out: L08, L10, L16, L18, L19 (vertical).

**L10. Tokenization and language modeling: a GPT from scratch** (arch, 10 h, Colab)
- Derive: language modeling as next-token cross-entropy, BPE algorithm, sampling (temperature, top-k, top-p), perplexity.
- Build: BPE tokenizer from scratch, data loader, GPT model, training loop with eval, sampling.
- Break: tokenizer edge cases (whitespace, unicode); temperature extremes.
- Capstone: train a small GPT on a provided public-domain corpus and report validation loss and samples.
- Edges in: L09, M27 (vertical); L13 (horizontal). Edges out: L11, L12 (vertical).

**L13. Mixed precision and floating-point numerics** (sys, 7 h, Colab)
- Derive: IEEE formats, bf16 vs fp16 range and precision, loss scaling, stochastic rounding, accumulation precision, fp8 basics.
- Build: simulate formats in NumPy; mixed-precision training with autocast and GradScaler; measure speed and memory.
- Break: fp16 overflow in attention logits; underflow of small gradients.
- Capstone: convert the L10 GPT to bf16/fp16 training with matching loss and a measured speedup.
- Edges in: L07 (vertical); M26 (long-range). Edges out: L14, L18 (vertical); L10 (horizontal).

### Scale

**L11. Scaling laws and compute-optimal training** (llm, 9 h, Colab)
- Derive: power-law fits, the compute approximation C ≈ 6ND, compute-optimal allocation of parameters and tokens under a power-law loss model, why loss is predictable.
- Build: train a sweep of tiny GPTs (L10 code) at several sizes and token counts, fit power laws, find the compute-optimal frontier on your own data.
- Break: fitting on too narrow a range; ignoring learning-rate retuning across sizes.
- Capstone: predict the loss of a held-out larger run before training it, then compare.
- Edges in: L02, L05, L10 (vertical); L12, M35 (horizontal). Edges out: L14, L15 (vertical); L20 (long-range).

**L12. Data at scale: curation, dedup, mixtures, pipelines** (sys, 8 h, browser + Colab)
- Derive: why data quality changes scaling, near-duplicate detection with MinHash and LSH (derive collision probability), mixture weighting, train/eval contamination.
- Build: MinHash dedup, quality heuristics, a sharded streaming data loader with deterministic resumption.
- Break: contamination inflating eval scores; non-deterministic shuffles breaking resumption.
- Capstone: a pipeline that dedups and filters a provided corpus and shows a validation-loss improvement on L10's model.
- Edges in: L10 (vertical); L02 (long-range). Edges out: L15 (vertical); L11 (horizontal).

**L14. Distributed training: DDP, FSDP/ZeRO, tensor and pipeline parallel** (sys, 12 h, Colab)
- Derive: memory accounting (weights, grads, optimizer states, activations), all-reduce, reduce-scatter, all-gather costs, ZeRO stages 1 to 3, tensor parallel matmul splits, pipeline bubbles, activation checkpointing.
- Build: simulated multi-process DDP and ZeRO on CPU with `torch.distributed` (gloo); tensor-parallel linear layer; activation checkpointing; the `ParallelismPlanner` exercises for real model sizes.
- Break: deadlocks from mismatched collectives; wrong gradient averaging.
- Capstone: a written parallelism plan for a stated model size and cluster, with memory math verified by the planner and a working simulated implementation.
- Edges in: L07, L11, L13 (vertical); L04 (long-range). Edges out: L15 (vertical).

**L15. A real pretraining run: loss spikes, checkpoints, eval harness** (sys, 11 h, Colab)
- Derive: what causes loss spikes (LR, data, numerics, attention logit growth), gradient clipping, z-loss, checkpoint and resume semantics.
- Build: a full training script with config, logging, checkpointing and exact resume, an eval harness, spike detection and rollback.
- Break: injected bad data batch; injected LR bug; resume that silently changes data order.
- Capstone: run a multi-hour GPT pretraining on Colab with logged metrics, recover from an injected spike, and write a run report.
- Edges in: L11, L12, L14 (vertical); L05 (long-range). Edges out: L16, L20 (vertical).

### Frontier

**L16. Fine-tuning: SFT, LoRA, distillation** (llm, 9 h, Colab)
- Derive: supervised fine-tuning objective with loss masking, catastrophic forgetting, LoRA as low-rank update (link to SVD), knowledge distillation with temperature.
- Build: SFT on the L15 model with a provided instruction set, LoRA from scratch, distillation from a larger to a smaller model.
- Break: training on prompt tokens; LoRA rank too low; forgetting measured on base evals.
- Capstone: a LoRA fine-tune that hits a target metric while keeping base eval loss within a stated margin.
- Edges in: L09, L15 (vertical); M14 (long-range). Edges out: L17, L20 (vertical); L18 (horizontal).

**L17. RL for language models: policy gradients, RLHF, DPO, verifiable rewards** (llm, 12 h, Colab)
- Derive: policy gradient theorem, REINFORCE with baselines, advantage estimation, PPO clipped objective, KL penalty to reference, reward models from preferences (Bradley-Terry), DPO derivation from the KL-regularized objective, RL with verifiable rewards.
- Build: REINFORCE on a toy bandit and a small LM, a Bradley-Terry reward model, DPO training, RL on arithmetic tasks with an exact-match reward.
- Break: reward hacking with a flawed reward; removing the KL penalty.
- Capstone: improve the L16 model's accuracy on a provided verifiable task with RL and report the reward-KL tradeoff.
- Edges in: L16 (vertical); M36 (horizontal); L03, M27, M30 (long-range). Edges out: L19, L20 (vertical).

**L18. Inference systems: KV cache, batching, quantization, speculative decoding** (sys, 10 h, Colab)
- Derive: prefill vs decode cost, KV cache memory formula, continuous batching, paged attention idea, int8/int4 weight quantization error, speculative decoding acceptance rule and why it preserves the distribution.
- Build: KV-cache generation for the L10 model, a continuous-batching scheduler simulation, weight-only int8 quantization, speculative decoding with a draft model, latency and throughput benchmarks.
- Break: cache index bugs; quantization outliers.
- Capstone: an inference server loop that meets stated latency and throughput targets on the T4.
- Edges in: L08, L09, L13 (vertical); L16 (horizontal). Edges out: L20 (vertical).

**L19. Evaluation and interpretability: probes, sparse autoencoders, circuits** (llm, 10 h, Colab)
- Derive: eval design (contamination, variance, confidence intervals over items), linear probes, superposition intuition, sparse autoencoder objective, activation patching logic.
- Build: an eval harness with bootstrap CIs, linear probes on the L15 model, a sparse autoencoder on its activations, activation patching on a toy task such as induction.
- Break: an eval with too few items; a probe that succeeds on random features.
- Capstone: find and validate an interpretable circuit or feature set in your model, with a written report.
- Edges in: L09, L17 (vertical); M25 (long-range). Edges out: L20 (vertical).

**L20. Capstone: train, align, evaluate and serve a small LM** (all, 12 h, Colab)
- No new theory; the theory half is a written design document defending every choice with references to earlier lessons (graded by the Feynman grader with a design rubric).
- Practice half: from raw corpus to served model: data pipeline (L12), pretrain (L15), fine-tune (L16), RL (L17), evaluate (L19), serve (L18), with a final report.
- Edges in: L15, L16, L17, L18, L19 (vertical); M38 (horizontal); L11 (long-range). Edges out: none.

### Full edge list (as encoded in `graph.yaml`)
Every edge that touches a lesson of this section; the math track's edges among its own lessons are in `docs/math-track.md`.

Vertical: M12-L01, M19-L03, M19-L04, M25-L01, M25-L02, M27-L02, M27-L10, M28-L05, L01-L02, L01-L03, L02-L11, L03-L04, L03-L05, L03-L09, L04-L07, L05-L06, L05-L11, L06-L09, L07-L08, L07-L13, L07-L14, L09-L08, L09-L10, L09-L16, L09-L18, L09-L19, L10-L11, L10-L12, L11-L14, L11-L15, L12-L15, L13-L14, L13-L18, L14-L15, L15-L16, L16-L17, L17-L19, L08-L18, L15-L20, L16-L20, L17-L20, L18-L20, L19-L20.
Horizontal: M30-L01 (ridge regression is a Lagrangian with a norm constraint), M31-L02 (concentration bounds put numbers on the generalization gap), M29-L05 (proved rates meet the practical optimizers), M34-L06 (variance preservation is what initialization and normalization protect), M33-L07 (arithmetic intensity places each kernel on the roofline), M34-L09 (near-orthogonality explains the 1/sqrt(d) in attention), M35-L11 (your fitting machinery produces the scaling-law fit), M36-L17 (REINFORCE is the policy-gradient estimator behind RLHF), M38-L20 (the paper audit method is applied to your capstone model), L04-L05 (your autograd engine drives the optimizers), L07-L09 (attention cost read on the roofline), L12-L11 (data quality shifts the scaling curve), L13-L10 (train the GPT in reduced precision), L06-L08 (the layer norm derived here becomes a fused kernel), L16-L18 (a distilled student is a natural speculative-decoding draft).
Long-range: M04-L03 (sums of shifted ReLUs return as one-hidden-layer networks), M07-L09 (planar rotations return as rotary position embeddings), M10-L09 (matrix products are the whole of attention's compute), M14-L16 (SVD returns as the low-rank update in LoRA), M25-L19 (the bootstrap returns as confidence intervals on evals), M26-L13 (machine epsilon returns as the limits of bf16 and fp8), M27-L17 (KL divergence returns as the RLHF penalty), M30-L17 (the KL-regularized optimum returns as the basis of DPO), L05-L15 (learning-rate schedules return in spike recovery), L01-L09 (softmax returns as attention weights), L02-L12 (test-set leakage returns as train/eval contamination), L03-L17 (the gradient p - y returns as the policy-gradient score function), L04-L14 (tensors saved for backward return as activation memory), L11-L20 (your scaling fit sizes the capstone model and token budget).

---

## 11. Commands and CI

| Command | Does |
| --- | --- |
| `npm run dev` | Local dev server |
| `npm run build` | `build_content.ts`, then Vite build to `dist/` |
| `npm run validate` | `validate_content.ts` |
| `npm run test` | Vitest unit tests |
| `npm run e2e` | Playwright: open map, open a lesson, pass one exercise, see progress persist after reload |
| `npm run e2e:path` | Playwright: a simulated learner completes every lesson in prerequisite order with the solutions |
| `npm run pytest` | `run_exercise_tests.py`: every `solution.py` passes its `tests.py`; every `starter.py` fails at least one test |
| `npm run notebooks` | `run_notebooks.py` with `SMALL=1` |
| `npm run check` | validate + typecheck + lint + test + pytest + build (notebooks run in CI only) |

`check.yml`: Node 20 and Python 3.11; runs `npm run check` and `npm run notebooks`. `deploy.yml`: on `main`, build and publish `dist/` to GitHub Pages. The repository is `2Syuretto7/Forge` and Pages paths are case-sensitive, so Vite `base` is the relative `./` (works under `/Forge/` and any other path with the hash router) and Colab links use `2Syuretto7/Forge`.

Implementation notes (decided during Phase 1):
- Pyodide core files come from the pinned `pyodide` npm package; the matching NumPy wheel is vendored in `vendor/pyodide/` and checked against `pyodide-lock.json` by SHA-256. Everything is served from the site itself, so the app makes no CDN calls.
- Notebooks are authored as percent-format Python in the GPU lesson's `capstone/solution.py` (cells split on `# %%`, solution regions between `# BEGIN SOLUTION` and `# END SOLUTION`, with an optional `-> replacement` for the learner version), next to `capstone/tests.py`, which becomes the autograder cell. `build_content.ts` writes the learner `.ipynb` to `notebooks/<ID>.ipynb` (committed, so Colab can open it from `main`) and the solved version to `notebooks/solved/<ID>.ipynb` (also committed: CI executes it, and `docs/colab-check.md` has the owner's one-click T4 check).
- `:::colab{notebook=<ID> runtime=cpu}` marks a notebook that needs no GPU (L04); the button text and the notebook metadata then leave the accelerator unset.
- A retro-annotation may name its target movement (`{target: L03, movement: m2-derivation, anchor: ..., text: ...}`); the anchor is matched case-insensitively against the plain text of that movement's blocks, first match wins.
- Exercise hints live at the end of `prompt.md` under a `## Hints` heading (numbered list, at most 3).
- Deployment: `deploy.yml` publishes from `main` and, until `main` exists, from the working branch. The build receives `VITE_COLAB_BRANCH` (the branch it built from), so the Colab button opens the notebooks committed next to the deployed site.
- Widgets beyond Section 7: `LshCurve` (L12) plots the LSH candidate probability for chosen bands and rows. `LossSpikeExplorer` replays real logged CPU runs written by `scripts/gen_spike_runs.py` into `src/widgets/data/spike_runs.json`.
- L11's sweep is sized for Tiny Shakespeare (the only corpus the notebooks can verify offline): four layers at five widths, every run 1,950 steps with the batch growing with the token budget, at most four epochs. At this scale the runs are early in training and the fitted floor $E$ is constrained to be non-negative; the held-out prediction must land within 8%.
- L14's capstone needs no GPU: four CPU processes joined by `torch.distributed` (gloo) through `fork`, using only `all_reduce`, `all_gather` and point-to-point messages, which every PyTorch version's gloo backend supports.
- L15's reference run is the nanoGPT-sized character model for 5,000 steps, roughly 15 to 25 minutes on a T4 rather than several hours: a longer run on Tiny Shakespeare would only overfit. The script checkpoints to Google Drive when mounted and resumes after a disconnection, so the same code serves a multi-hour run on a larger corpus.
- L16's capstone replays pretraining text during fine-tuning (both LoRA and full fine-tuning): without it, measured forgetting on the small pretrained model was over 1.9 nats per byte for either method, so the "forgetting margin" target is only meaningful with replay.
- L17's capstone fine-tunes on demonstrations of two-digit addition in which 30% of answers contain a slip, then runs RL against an exact verifier. Clean addition is mastered by supervision alone, and on harder tasks (multiplication) RL mostly sharpened memorized answers; noisy demonstrations give the verifier something it reliably fixes and make the reward-KL tradeoff monotone. The KL penalty uses the `exp(u) - 1 - u` estimator, whose gradient is that of KL(reference || policy); the reported KL is computed exactly per position.
- L18 compares throughput at saturation (all requests queued) and measures latency on the arriving workload: with arrivals at a fixed rate, throughput is capped by the arrivals rather than the server.
- L19's toy model uses relative position biases instead of absolute position embeddings. With absolute positions the same task is solved by a different circuit (a layer-0 head that finds the earlier copy of the current token and copies its position); relative positions leave the classic previous-token head plus induction head. The notebook mentions both.
- L20 provides the solved tools of L12 to L18 and asks the learner for the plan, the cleaning order, the stage evaluation, the reward, the manifest and the report.

---

## 12. Acceptance criteria (the plan is complete only when all hold)

1. The deployed site opens at `https://<owner>.github.io/forge/` with no console errors.
2. The map shows 24 nodes and all edges in Section 10, with the three edge styles and toggles.
3. All 24 lessons are complete per the validator, with 6 to 12 hours each, 45 to 55% theory, at least 12 exercises plus a capstone.
4. Every exercise's solution passes and starter fails in CI. Every notebook executes in `SMALL=1` mode in CI.
5. Every GPU notebook opens in Colab from its button and prints a valid completion code that the app accepts.
6. Feynman grading works with a valid key and degrades gracefully without one.
7. Reviews: completing a lesson schedules review items; due items appear in `#/review` and in the next lesson's recall bridge.
8. Retro-annotations appear in earlier lessons after later lessons are completed.
9. Progress survives reload, and export/import round-trips exactly.
10. Lighthouse accessibility score at least 90 on map and lesson pages; usable at 380px width.

---

## 13. Task list (execute in order; tick as done)

### Phase 1: Skeleton and the first lesson (owner can start learning at the end of this phase)
- [x] 1.1 Scaffold repo, tooling, CI (`check.yml`, `deploy.yml`), README.
- [x] 1.2 Content pipeline: `graph.yaml` with all 24 lessons and all edges; `build_content.ts`; `validate_content.ts` with every rule (lessons not yet written are allowed only under a `--phase` flag that lists the lessons expected so far).
- [x] 1.3 IndexedDB store and Settings screen (key, model, theme, export/import, reset).
- [x] 1.4 Map view with layered layout, node states, edge styles, toggles, mobile list mode.
- [x] 1.5 Lesson player: movements, directives (all of 6.3), edge markers, theory/practice meter.
- [x] 1.6 Pyodide worker, CodeMirror pane, test runner, hints, solution reveal.
- [x] 1.7 Prediction blocks and derivation step checker.
- [x] 1.8 Widgets used by the first lesson (`MatrixTransform`).
- [x] 1.9 Write the first lesson completely; pytest passes.
- [x] 1.10 Deploy; run acceptance checks 1, 2, 9 for the current scope; send the owner the URL.

### Phase 2: Math and Core ML (the other original math lessons, and L01 to L05)
- [x] 2.1 Feynman grader (Section 9) with fallback self-assessment.
- [x] 2.2 Spaced-review engine, `gen_reviews.ts`, `#/review`, recall-bridge integration.
- [x] 2.3 Colab button, completion-code verification, notebook autograder template.
- [x] 2.4 Widgets: `DistributionPlayground`, `ComputationGraph`, `EntropyBars`, `DecisionBoundary`, `BiasVarianceCurve`, `LossLandscape`, `ActivationStats`.
- [x] 2.5 Write the other three original math lessons.
- [x] 2.6 Write L01, L02, L03.
- [x] 2.7 Write L04 (browser part and notebook), L05.
- [x] 2.8 Retro-annotations engine.
- [x] 2.9 Deploy; acceptance checks for current scope.

### Phase 3: Architectures and Systems (L06 to L10, L13)
- [x] 3.1 Widgets: `Roofline`, `AttentionHeatmap`, `TokenizerStepper`, `FloatFormats`.
- [x] 3.2 Write L06, L07.
- [x] 3.3 Write L09, then L08 (L08 depends on L09).
- [x] 3.4 Write L10, L13.
- [x] 3.5 Notebooks for L07, L08, L09, L10, L13 pass in CI `SMALL=1`; manually verify one on a Colab T4 by running it yourself if you have access, otherwise document the exact runtime check the owner performs with one click.
- [x] 3.6 Deploy; acceptance checks for current scope.

### Phase 4: Scale (L11, L12, L14, L15)
- [x] 4.1 Widgets: `ScalingFit`, `ParallelismPlanner`, `LossSpikeExplorer`.
- [x] 4.2 Write L11, L12.
- [x] 4.3 Write L14, L15.
- [x] 4.4 Notebooks pass in CI; deploy; acceptance checks.

### Phase 5: Frontier (L16 to L20)
- [x] 5.1 Widgets: `RewardKLTradeoff`, `KVCacheMeter`, `FeatureDictionary`.
- [x] 5.2 Write L16, L17.
- [x] 5.3 Write L18, L19.
- [x] 5.4 Write L20 with the design-document rubric.
- [x] 5.5 Remove the `--phase` flag; full validator must pass for all 24 lessons.

### Phase 6: Hardening and handoff
- [x] 6.1 Full Playwright suite across a complete simulated learner path (every lesson with solutions).
- [x] 6.2 Accessibility and mobile pass (Lighthouse at least 90).
- [x] 6.3 Content review pass: re-read every derivation; every numeric claim backed by a test or a derivation in the lesson.
- [ ] 6.4 Run all 10 acceptance criteria; fix until all pass.
- [x] 6.5 Final README for the owner: the site URL, how to add the API key, how to open Colab lessons. Nothing else.
- [x] 6.6 Owner request: bring the interface closer to Codecademy and DataCamp (Section 5.0 and 5.2): dashboard with Resume, XP and streak; split-screen exercise workspace; lesson step bar, syllabus drawer and Back/Next bar.

### Phase 7: The math track (owner request; docs/math-track.md)
- [x] 7.1 Schema and validator: `prelude` stage, strands, the 38 lessons and 120 edges merged into `graph.yaml` with the original math lessons still present; validator rule 9 and 10; slow-and-steady gating and one-week closure in the store; a one-time progress reset when the new curriculum first loads (owner request, replacing the migration of docs/math-track.md); map with strand columns; unit and end-to-end tests.
- [x] 7.2 Prelude, M01 to M08, with their eight widgets.
- [x] 7.3 Foundations linear algebra and calculus, M09 to M20, with their widgets; move the material of the original linear-algebra and calculus lessons into M12, M14, M15, M18 and M19, and retire them. (The linear-algebra lesson's exercises went to M09 and M12 to M14, with its Rayleigh-gradient exercise in M18 and its low-rank training exercise in M19, after calculus; the calculus lesson's to M15, M18 and M19.)
- [x] 7.4 Foundations probability and numerics, M21 to M28, with their widgets; move the material of the original probability and information-theory lessons into M22, M24, M25 and M27, and retire them. (The probability lesson's exercises went to M22 (three), M24 (the CLT simulator) and M25 (eight, with the A/B capstone); the information-theory lesson went whole into M27, with two new exercises. New widgets BayesGrid, GaussianEllipse and CLTMachine; DistributionPlayground gained the exponential and Poisson families.)
- [x] Owner request, after 7.4: number the core lessons from L01. The lessons that were L05 to L24 became L01 to L20 everywhere (folders, graph, cross-references, notebooks, Colab codes, tests, this plan and the math-track spec), and progress saved under the earlier numbers is carried over once, at startup or on import.
- [x] 7.5 Learning stage, M29 to M32, with chips into L01, L02 and L05. (New widgets ConvergenceRates, KKTGeometry, ConcentrationMeter, BiasVarianceCurve and MarkovChainSim.)
- [x] 7.6 M33 to M37 beside their L-lesson partners; M38; retro-annotations from every M lesson into its predecessors; remove `--allow-unpublished`; full check, learner path and deploy. (New widgets RandomSpectrum, EstimatorVariance and DiffusionStepper; M33 reuses Roofline and SpectrumBars, M35 ScalingFit, M36 RewardKLTradeoff, M38 ComputationGraph. M38 offers three papers, DPO, LoRA and Adam, and its capstone checks the learner's lesson map against the curriculum graph.)

---

## 14. What to report to the owner

At the end of each phase, send one short message: the live URL, which lessons are now available, and anything you need from them (normally nothing). Do not send logs, diffs, or step-by-step narration.
