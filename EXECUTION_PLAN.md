# Forge: Execution Plan for the AI Coding Agent

This file is the complete, self-contained specification for building **Forge**, a personal learning platform for the ML research and ML engineering skills expected at frontier AI labs. Read it fully before writing code. Execute the phases in order. Do not stop at a partial build: every phase ends with a working, deployed app, and the plan is finished only when all 24 lessons pass the acceptance checks in Section 12.

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
| Pace | Content for all 24 lessons is built; the app unlocks by prerequisites, not by calendar. |
| Compute | Browser only (Pyodide + NumPy) for 9 lessons, browser plus Colab for 3 (L08, L13, L16), free Google Colab (T4 GPU) for 12. No paid compute required. |
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
- **Graph rule:** three edge types (vertical prerequisite, horizontal same-stage cross-track, long-range). Every lesson has at least 1 inbound edge (except L01 to L03), at least 1 outbound edge (except L24), and at least 1 horizontal or long-range edge. Enforced by the validator.

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
      L02/ ... L24/
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

### 5.1 Map (home, route `#/`)
- Full-screen graph. Columns = 5 tracks (Math, Core ML, Architectures, Systems (MLE), LLM science). Rows = 5 stages (Foundations, Learning, Models + GPUs, Scale, Frontier).
- Node states: locked (prerequisites incomplete, still clickable for preview), available, in progress (ring shows percent), complete.
- Edges: vertical = solid gray arrow; horizontal = solid colored double arrow; long-range = dashed colored arrow. Toggle each type on/off.
- Hover a node: title, hours, theory/practice split, prerequisites, unlocks. Click: open lesson.
- Header shows: total hours done / total, reviews due today (click to start), Settings.
- Works on phone width (380px): map becomes a stage-by-stage list with edges listed as chips.

### 5.2 Lesson player (route `#/lesson/:id/:movement?`)
- Left: movement navigator with theory/practice tag and estimated minutes per movement; a live theory/practice meter for the lesson.
- Center: the movement content (markdown + math + widgets + exercises).
- Right (desktop) or bottom sheet (mobile): code pane for the active exercise, test output, hints.
- Edge markers render inline as chips: "Reuses L04: KL divergence" (links back) and "Returns in L21" (links forward; disabled until reachable, shows a one-line teaser).
- Retro-annotations: when a later lesson is complete, its annotations appear as margin notes in earlier lessons.
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
- Due reviews also appear as each lesson's Movement 0 (recall bridge), filtered to that lesson's prerequisites.

### 5.8 Settings (route `#/settings`)
- API key (masked, stored locally, "Test key" button), model ID, theme, export progress JSON, import progress JSON, reset progress (with typed confirmation).

---

## 6. Content format

### 6.1 `content/graph.yaml`
```yaml
tracks: [math, core, arch, sys, llm]
stages: [foundations, learning, models_gpus, scale, frontier]
lessons:
  - id: L01
    title: Linear algebra as the geometry of data
    track: math
    stage: foundations
    gpu: false
edges:
  - {from: L01, to: L05, type: vertical}
  - {from: L13, to: L11, type: horizontal, note: "Attention cost read on the roofline"}
  - {from: L04, to: L21, type: long_range, note: "KL divergence returns as the RLHF penalty"}
```
The full lesson and edge list is in Section 10; encode it exactly.

### 6.2 `lesson.yaml`
```yaml
id: L13
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
  - {to: L12, text: "You will fuse this softmax into one kernel."}
reuses:       # backward links; drive Movement 0
  - {from: L07, concept: backprop through matrix products}
annotations:  # retro-annotations placed into earlier lessons when this lesson completes
  - {target: L05, anchor: softmax, text: "Softmax here is the same function that weights attention in L13."}
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

---

## 7. Interactive widgets (build all; reused across lessons)

| Widget | Shows | Used in |
| --- | --- | --- |
| `MatrixTransform` | 2D linear map acting on a grid and unit circle; SVD axes overlay | L01, L20 |
| `DistributionPlayground` | Sample, fit by MLE, see likelihood surface | L02, L06 |
| `ComputationGraph` | Forward values and backward gradients flowing on a graph | L03, L07, L08 |
| `EntropyBars` | Entropy, cross-entropy, KL between two editable distributions | L04, L14, L21 |
| `DecisionBoundary` | Logistic regression boundary training live | L05 |
| `BiasVarianceCurve` | Train/test error vs capacity, double-descent regime | L06, L15 |
| `LossLandscape` | 2D loss surface with SGD/momentum/Adam trajectories | L09 |
| `ActivationStats` | Per-layer activation and gradient histograms under different inits and norms | L09, L10 |
| `Roofline` | Arithmetic intensity vs achievable FLOP/s; place kernels on it | L11, L12, L13, L22 |
| `AttentionHeatmap` | Q, K, V and attention weights for a toy sequence; causal mask toggle | L13, L23 |
| `TokenizerStepper` | BPE merges step by step | L14 |
| `ScalingFit` | Fit power laws to loss vs compute; compute-optimal frontier | L15 |
| `FloatFormats` | Bit layout and rounding of fp32, bf16, fp16, fp8 | L17, L22 |
| `ParallelismPlanner` | Memory per GPU for DP, ZeRO stages, TP, PP given model size | L18, L19 |
| `LossSpikeExplorer` | Replay a logged training run; inspect grad norm, LR, spikes | L19 |
| `KVCacheMeter` | KV cache memory vs batch, length, heads, precision | L22 |
| `RewardKLTradeoff` | Reward vs KL-to-reference as beta changes | L21 |
| `FeatureDictionary` | Sparse autoencoder features over toy activations | L23 |

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

## 10. Curriculum: all 24 lessons

Every lesson follows the movement pattern in 6.2 (recall bridge, puzzle, derivation, build, scale/measure, break it, Feynman, capstone). Hours, content, edges and capstones below are binding. "Exercises" lists the minimum set; add more to reach at least 12 per lesson.

### Stage 1: Foundations

**L01. Linear algebra as the geometry of data** (math, 8 h, browser)
- Puzzle: why does solving a nearly singular system return garbage, and why do embeddings live on a few directions?
- Derive: vector spaces, bases, projections, least squares via normal equations, eigendecomposition, SVD from scratch, condition number, low-rank approximation (Eckart-Young statement and numeric check).
- Build: Gram-Schmidt, QR, power iteration, SVD via eigendecomposition of AᵀA, PCA on synthetic data, rank-k compression of an image array.
- Break: solve ill-conditioned systems in float32 vs float64; compare normal equations with QR.
- Capstone: PCA pipeline that explains 95% variance on a provided synthetic embedding set, with a written interpretation of the top 3 components.
- Edges out: L05 (vertical), L09 (vertical), L13 (vertical), L20 (long-range, SVD to LoRA).

**L02. Probability, likelihood and estimation** (math, 8 h, browser)
- Puzzle: two coins, few flips; how confident should you be?
- Derive: random variables, expectation, variance, Gaussian and Bernoulli/categorical, Bayes' rule, MLE for Bernoulli and Gaussian, MAP with priors, bias of estimators, law of large numbers and CLT (simulation-backed).
- Build: samplers from uniform, MLE fitters, bootstrap confidence intervals, a Monte Carlo CLT demo.
- Break: MLE with tiny samples; heavy-tailed data breaks the sample mean.
- Capstone: A/B test analyzer with bootstrap and Bayesian posteriors, with a report on when they disagree.
- Edges out: L04, L05, L06 (vertical).

**L03. Calculus, Jacobians and automatic differentiation** (math, 8 h, browser)
- Puzzle: why does finite-difference gradient checking fail at step size 1e-12?
- Derive: derivatives, chain rule, partial derivatives, gradients, Jacobians, vector-Jacobian products, forward vs reverse mode cost, Taylor expansion and why gradient descent works locally.
- Build: numeric differentiation with error analysis, forward-mode autodiff with dual numbers, Jacobians of softmax, layer norm and matrix multiply by hand, verified numerically.
- Break: step-size sweep showing truncation vs rounding error.
- Capstone: dual-number autodiff library that differentiates a 20-line function, verified against finite differences.
- Edges out: L07, L08 (vertical). Horizontal: L04.

**L04. Information theory: entropy, cross-entropy, KL** (math, 7 h, browser)
- Puzzle: why is the training loss of a language model measured in nats, and what does 1.5 nats mean?
- Derive: surprisal, entropy, cross-entropy, KL divergence and its asymmetry, Gibbs' inequality, mutual information, the link between MLE and minimizing cross-entropy, perplexity.
- Build: entropy estimators, KL between Gaussians (closed form vs Monte Carlo), cross-entropy loss with log-sum-exp stability.
- Break: naive softmax cross-entropy overflowing; forward vs reverse KL fitting a bimodal target.
- Capstone: a compression experiment: Huffman code a text corpus and compare bits per character with entropy estimates.
- Edges in: L02. Edges out: L06, L14 (vertical), L21 (long-range).

### Stage 2: Learning

**L05. Linear and logistic regression, end to end** (core, 8 h, browser)
- Derive: least squares from MLE under Gaussian noise; logistic regression from Bernoulli MLE; gradients of both; softmax regression; L2 as Gaussian prior.
- Build: closed-form and gradient-descent solvers, softmax classifier, feature standardization, evaluation metrics (accuracy, log loss, calibration curve).
- Break: unscaled features, perfectly separable data driving weights to infinity.
- Capstone: multi-class classifier on a provided tabular dataset reaching a stated accuracy, with calibration analysis.
- Edges in: L01, L02. Edges out: L06, L07.

**L06. Generalization, bias-variance and double descent** (core, 7 h, browser)
- Derive: train/test split rationale, bias-variance decomposition for squared error, regularization, cross-validation, overparameterized interpolation and double descent with random features.
- Build: polynomial and random-feature regressions, k-fold CV, a double-descent curve.
- Break: test-set leakage; tuning on the test set.
- Capstone: reproduce a double-descent curve and explain where the peak sits.
- Edges in: L02, L04, L05. Edges out: L15 (vertical).

**L07. Neural networks and backprop from scratch** (core, 10 h, browser)
- Derive: MLP forward pass, universal approximation intuition, backprop as reverse-mode autodiff on matrix expressions, gradients for linear, ReLU, tanh, softmax-cross-entropy.
- Build: NumPy MLP with manual backward, gradient checks per layer, minibatch training on a provided spiral and digit-like dataset.
- Break: all-zero init symmetry; dead ReLUs; exploding activations from bad init.
- Capstone: 2-hidden-layer MLP reaching a stated accuracy, all gradients written by hand.
- Edges in: L03, L05. Edges out: L08, L09, L13.

**L08. Build a mini autograd engine; PyTorch internals** (sys, 10 h, browser + Colab)
- Derive: computation graphs, topological sort, tensor broadcasting rules and their gradients, memory saved for backward.
- Build: tensor autograd engine in NumPy (add, mul, matmul, sum, exp, log, relu, broadcasting, reshape), with an `nn.Module`-like API; train the L07 MLP on it. In Colab: compare against PyTorch, inspect `grad_fn`, write a custom `torch.autograd.Function`.
- Break: in-place ops corrupting saved tensors; broadcasting gradient bugs.
- Capstone: the engine trains an MLP to match the PyTorch reference loss curve within tolerance.
- Edges in: L03, L07. Edges out: L11. Horizontal: L09.

**L09. Optimization: SGD, momentum, Adam, schedules, initialization** (core, 9 h, browser)
- Derive: gradient descent on quadratics and condition number, momentum as a low-pass filter, RMSProp and Adam with bias correction, AdamW decoupled weight decay, warmup and cosine schedules, Xavier and He initialization from variance preservation.
- Build: each optimizer from scratch; schedule functions; init schemes; compare on the `LossLandscape` widget and on the L07 MLP.
- Break: learning rate too high; Adam without bias correction early in training; weight decay vs L2 inside Adam.
- Capstone: an optimizer bake-off report with a tuned recipe for the L07 task.
- Edges in: L01, L07. Edges out: L10, L15.

### Stage 3: Models + GPUs

**L10. Normalization, residuals and training stability** (arch, 8 h, browser)
- Derive: batch norm and layer norm forward and backward, RMSNorm, residual connections and gradient flow through depth, pre-norm vs post-norm.
- Build: each norm with manual backward and gradient checks; a 20-layer MLP with and without residuals and norms; activation statistics tracking.
- Break: post-norm deep stacks without warmup; batch norm with batch size 1.
- Capstone: train a 30-layer residual MLP stably and explain each stabilizing choice.
- Edges in: L09. Edges out: L13.

**L11. GPU architecture and the roofline model** (sys, 9 h, Colab)
- Derive: SMs, warps, memory hierarchy (registers, shared, L2, HBM), bandwidth vs compute bound, arithmetic intensity, roofline; FLOP counts for matmul and elementwise ops.
- Build: benchmark matmul and elementwise ops on the T4, place them on a measured roofline; profile with `torch.profiler`; measure the cost of host-device transfers.
- Break: tiny kernels dominated by launch overhead; unnecessary `.item()` syncs.
- Capstone: a profiling report that explains a provided slow training step and speeds it up by at least 2x.
- Edges in: L08. Edges out: L12, L17, L18. Horizontal: L13.

**L12. Writing kernels: Triton, fused ops, FlashAttention** (sys, 11 h, Colab)
- Derive: tiling, memory coalescing, kernel fusion savings, online softmax (derive the running max and sum update), FlashAttention's IO complexity.
- Build: Triton vector add, fused softmax, tiled matmul, fused layer norm, a forward FlashAttention kernel tested against a reference.
- Break: numerically unstable softmax in fp16; wrong block sizes.
- Capstone: FlashAttention forward kernel matching reference within 1e-2 in fp16 and faster than the naive version at sequence length 2048.
- Edges in: L11, L13. Edges out: L22.

**L13. Attention and the transformer from scratch** (arch, 11 h, browser + Colab)
- Derive: attention as soft lookup, scaled dot product (why divide by sqrt(d)), causal masking, multi-head attention, positional information (sinusoidal, RoPE), the full decoder block, parameter and FLOP counts.
- Build: NumPy attention with manual backward; permutation-equivariance tests; full decoder block in PyTorch in Colab.
- Break: missing scaling causing saturated softmax; mask off by one leaking the future.
- Capstone: train a 2-layer transformer on a provided public-domain character corpus to below a stated loss.
- Edges in: L01, L07, L10. Edges out: L12, L14, L20, L23. Horizontal: L11.

**L14. Tokenization and language modeling: a GPT from scratch** (arch, 10 h, Colab)
- Derive: language modeling as next-token cross-entropy, BPE algorithm, sampling (temperature, top-k, top-p), perplexity.
- Build: BPE tokenizer from scratch, data loader, GPT model, training loop with eval, sampling.
- Break: tokenizer edge cases (whitespace, unicode); temperature extremes.
- Capstone: train a small GPT on a provided public-domain corpus and report validation loss and samples.
- Edges in: L04, L13. Edges out: L15, L16.

**L17. Mixed precision and floating-point numerics** (sys, 7 h, Colab)
- Derive: IEEE formats, bf16 vs fp16 range and precision, loss scaling, stochastic rounding, accumulation precision, fp8 basics.
- Build: simulate formats in NumPy; mixed-precision training with autocast and GradScaler; measure speed and memory.
- Break: fp16 overflow in attention logits; underflow of small gradients.
- Capstone: convert the L14 GPT to bf16/fp16 training with matching loss and a measured speedup.
- Edges in: L11. Edges out: L18, L22.

### Stage 4: Scale

**L15. Scaling laws and compute-optimal training** (llm, 9 h, Colab)
- Derive: power-law fits, the compute approximation C ≈ 6ND, compute-optimal allocation of parameters and tokens under a power-law loss model, why loss is predictable.
- Build: train a sweep of tiny GPTs (L14 code) at several sizes and token counts, fit power laws, find the compute-optimal frontier on your own data.
- Break: fitting on too narrow a range; ignoring learning-rate retuning across sizes.
- Capstone: predict the loss of a held-out larger run before training it, then compare.
- Edges in: L06, L09, L14. Edges out: L18, L19.

**L16. Data at scale: curation, dedup, mixtures, pipelines** (sys, 8 h, browser + Colab)
- Derive: why data quality changes scaling, near-duplicate detection with MinHash and LSH (derive collision probability), mixture weighting, train/eval contamination.
- Build: MinHash dedup, quality heuristics, a sharded streaming data loader with deterministic resumption.
- Break: contamination inflating eval scores; non-deterministic shuffles breaking resumption.
- Capstone: a pipeline that dedups and filters a provided corpus and shows a validation-loss improvement on L14's model.
- Edges in: L14. Edges out: L19.

**L18. Distributed training: DDP, FSDP/ZeRO, tensor and pipeline parallel** (sys, 12 h, Colab)
- Derive: memory accounting (weights, grads, optimizer states, activations), all-reduce, reduce-scatter, all-gather costs, ZeRO stages 1 to 3, tensor parallel matmul splits, pipeline bubbles, activation checkpointing.
- Build: simulated multi-process DDP and ZeRO on CPU with `torch.distributed` (gloo); tensor-parallel linear layer; activation checkpointing; the `ParallelismPlanner` exercises for real model sizes.
- Break: deadlocks from mismatched collectives; wrong gradient averaging.
- Capstone: a written parallelism plan for a stated model size and cluster, with memory math verified by the planner and a working simulated implementation.
- Edges in: L11, L15, L17. Edges out: L19.

**L19. A real pretraining run: loss spikes, checkpoints, eval harness** (sys, 11 h, Colab)
- Derive: what causes loss spikes (LR, data, numerics, attention logit growth), gradient clipping, z-loss, checkpoint and resume semantics.
- Build: a full training script with config, logging, checkpointing and exact resume, an eval harness, spike detection and rollback.
- Break: injected bad data batch; injected LR bug; resume that silently changes data order.
- Capstone: run a multi-hour GPT pretraining on Colab with logged metrics, recover from an injected spike, and write a run report.
- Edges in: L15, L16, L18. Edges out: L20.

### Stage 5: Frontier

**L20. Fine-tuning: SFT, LoRA, distillation** (llm, 9 h, Colab)
- Derive: supervised fine-tuning objective with loss masking, catastrophic forgetting, LoRA as low-rank update (link to SVD), knowledge distillation with temperature.
- Build: SFT on the L19 model with a provided instruction set, LoRA from scratch, distillation from a larger to a smaller model.
- Break: training on prompt tokens; LoRA rank too low; forgetting measured on base evals.
- Capstone: a LoRA fine-tune that hits a target metric while keeping base eval loss within a stated margin.
- Edges in: L13, L19, L01 (long-range). Edges out: L21.

**L21. RL for language models: policy gradients, RLHF, DPO, verifiable rewards** (llm, 12 h, Colab)
- Derive: policy gradient theorem, REINFORCE with baselines, advantage estimation, PPO clipped objective, KL penalty to reference, reward models from preferences (Bradley-Terry), DPO derivation from the KL-regularized objective, RL with verifiable rewards.
- Build: REINFORCE on a toy bandit and a small LM, a Bradley-Terry reward model, DPO training, RL on arithmetic tasks with an exact-match reward.
- Break: reward hacking with a flawed reward; removing the KL penalty.
- Capstone: improve the L20 model's accuracy on a provided verifiable task with RL and report the reward-KL tradeoff.
- Edges in: L04 (long-range), L20. Edges out: L23.

**L22. Inference systems: KV cache, batching, quantization, speculative decoding** (sys, 10 h, Colab)
- Derive: prefill vs decode cost, KV cache memory formula, continuous batching, paged attention idea, int8/int4 weight quantization error, speculative decoding acceptance rule and why it preserves the distribution.
- Build: KV-cache generation for the L14 model, a continuous-batching scheduler simulation, weight-only int8 quantization, speculative decoding with a draft model, latency and throughput benchmarks.
- Break: cache index bugs; quantization outliers.
- Capstone: an inference server loop that meets stated latency and throughput targets on the T4.
- Edges in: L12, L13, L17. Edges out: L24.

**L23. Evaluation and interpretability: probes, sparse autoencoders, circuits** (llm, 10 h, Colab)
- Derive: eval design (contamination, variance, confidence intervals over items), linear probes, superposition intuition, sparse autoencoder objective, activation patching logic.
- Build: an eval harness with bootstrap CIs, linear probes on the L19 model, a sparse autoencoder on its activations, activation patching on a toy task such as induction.
- Break: an eval with too few items; a probe that succeeds on random features.
- Capstone: find and validate an interpretable circuit or feature set in your model, with a written report.
- Edges in: L13, L21. Edges out: L24.

**L24. Capstone: train, align, evaluate and serve a small LM** (all, 12 h, Colab)
- No new theory; the theory half is a written design document defending every choice with references to earlier lessons (graded by the Feynman grader with a design rubric).
- Practice half: from raw corpus to served model: data pipeline (L16), pretrain (L19), fine-tune (L20), RL (L21), evaluate (L23), serve (L22), with a final report.
- Edges in: L19, L20, L21, L22, L23. Edges out: none.

### Full edge list to encode in `graph.yaml`
Vertical: L01-L05, L01-L09, L01-L13, L02-L04, L02-L05, L02-L06, L03-L07, L03-L08, L04-L06, L04-L14, L05-L06, L05-L07, L06-L15, L07-L08, L07-L09, L07-L13, L08-L11, L09-L10, L09-L15, L10-L13, L11-L12, L11-L17, L11-L18, L13-L12, L13-L14, L13-L20, L13-L22, L13-L23, L14-L15, L14-L16, L15-L18, L15-L19, L16-L19, L17-L18, L17-L22, L18-L19, L19-L20, L20-L21, L21-L23, L12-L22, L19-L24, L20-L24, L21-L24, L22-L24, L23-L24.
Horizontal: L03-L04, L08-L09, L11-L13, L16-L15, L17-L14.
Long-range: L01-L20 (SVD to LoRA), L04-L21 (KL to RLHF), L02-L23 (bootstrap to eval CIs), L09-L19 (schedules to spike recovery), L05-L13 (softmax to attention), L07-L08 (manual backprop to autograd internals is vertical; do not duplicate), L06-L15 (already vertical; do not duplicate).

Only the first five long-range edges are new; the last two notes exist to prevent duplicates.

Added to satisfy the graph rule in Section 2 (the list above leaves L06, L07, L10, L12, L18, L22 and L24 without any horizontal or long-range edge; these six edges close that gap without removing anything above):
Horizontal: L10-L12 (the layer norm derived in L10 becomes a fused kernel in L12), L20-L22 (a distilled student is a natural speculative-decoding draft).
Long-range: L06-L16 (test-set leakage returns as train/eval contamination), L07-L21 (the softmax cross-entropy gradient p - y returns as the policy-gradient score function), L08-L18 (tensors saved for backward return as activation memory and checkpointing), L15-L24 (the scaling-law fit sizes the capstone model and token budget).

---

## 11. Commands and CI

| Command | Does |
| --- | --- |
| `npm run dev` | Local dev server |
| `npm run build` | `build_content.ts`, then Vite build to `dist/` |
| `npm run validate` | `validate_content.ts` |
| `npm run test` | Vitest unit tests |
| `npm run e2e` | Playwright: open map, open L01, pass one exercise, see progress persist after reload |
| `npm run pytest` | `run_exercise_tests.py`: every `solution.py` passes its `tests.py`; every `starter.py` fails at least one test |
| `npm run notebooks` | `run_notebooks.py` with `SMALL=1` |
| `npm run check` | validate + typecheck + lint + test + pytest + build (notebooks run in CI only) |

`check.yml`: Node 20 and Python 3.11; runs `npm run check` and `npm run notebooks`. `deploy.yml`: on `main`, build and publish `dist/` to GitHub Pages. The repository is `2Syuretto7/Forge` and Pages paths are case-sensitive, so Vite `base` is the relative `./` (works under `/Forge/` and any other path with the hash router) and Colab links use `2Syuretto7/Forge`.

Implementation notes (decided during Phase 1):
- Pyodide core files come from the pinned `pyodide` npm package; the matching NumPy wheel is vendored in `vendor/pyodide/` and checked against `pyodide-lock.json` by SHA-256. Everything is served from the site itself, so the app makes no CDN calls.
- Notebooks are authored as percent-format Python (`content/lessons/<ID>/notebook/notebook.py`, cells split on `# %%`, solution regions between `# BEGIN SOLUTION` and `# END SOLUTION`). `build_content.ts` writes the learner `.ipynb` to `notebooks/<ID>.ipynb` (committed, so Colab can open it from `main`) and the solved version to `build/notebooks/` for CI.
- Exercise hints live at the end of `prompt.md` under a `## Hints` heading (numbered list, at most 3).

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

### Phase 1: Skeleton and L01 (owner can start learning at the end of this phase)
- [x] 1.1 Scaffold repo, tooling, CI (`check.yml`, `deploy.yml`), README.
- [x] 1.2 Content pipeline: `graph.yaml` with all 24 lessons and all edges; `build_content.ts`; `validate_content.ts` with every rule (lessons not yet written are allowed only under a `--phase` flag that lists the lessons expected so far).
- [x] 1.3 IndexedDB store and Settings screen (key, model, theme, export/import, reset).
- [x] 1.4 Map view with layered layout, node states, edge styles, toggles, mobile list mode.
- [x] 1.5 Lesson player: movements, directives (all of 6.3), edge markers, theory/practice meter.
- [x] 1.6 Pyodide worker, CodeMirror pane, test runner, hints, solution reveal.
- [x] 1.7 Prediction blocks and derivation step checker.
- [x] 1.8 Widgets used by L01 (`MatrixTransform`).
- [x] 1.9 Write L01 completely; pytest passes.
- [ ] 1.10 Deploy; run acceptance checks 1, 2, 9 for the current scope; send the owner the URL.

### Phase 2: Math and Core ML (L02 to L09)
- [x] 2.1 Feynman grader (Section 9) with fallback self-assessment.
- [ ] 2.2 Spaced-review engine, `gen_reviews.ts`, `#/review`, recall-bridge integration.
- [ ] 2.3 Colab button, completion-code verification, notebook autograder template.
- [x] 2.4 Widgets: `DistributionPlayground`, `ComputationGraph`, `EntropyBars`, `DecisionBoundary`, `BiasVarianceCurve`, `LossLandscape`, `ActivationStats`.
- [x] 2.5 Write L02, L03, L04.
- [ ] 2.6 Write L05, L06, L07.
- [ ] 2.7 Write L08 (browser part and notebook), L09.
- [ ] 2.8 Retro-annotations engine.
- [ ] 2.9 Deploy; acceptance checks for current scope.

### Phase 3: Architectures and Systems (L10 to L14, L17)
- [ ] 3.1 Widgets: `Roofline`, `AttentionHeatmap`, `TokenizerStepper`, `FloatFormats`.
- [ ] 3.2 Write L10, L11.
- [ ] 3.3 Write L13, then L12 (L12 depends on L13).
- [ ] 3.4 Write L14, L17.
- [ ] 3.5 Notebooks for L11, L12, L13, L14, L17 pass in CI `SMALL=1`; manually verify one on a Colab T4 by running it yourself if you have access, otherwise document the exact runtime check the owner performs with one click.
- [ ] 3.6 Deploy; acceptance checks for current scope.

### Phase 4: Scale (L15, L16, L18, L19)
- [ ] 4.1 Widgets: `ScalingFit`, `ParallelismPlanner`, `LossSpikeExplorer`.
- [ ] 4.2 Write L15, L16.
- [ ] 4.3 Write L18, L19.
- [ ] 4.4 Notebooks pass in CI; deploy; acceptance checks.

### Phase 5: Frontier (L20 to L24)
- [ ] 5.1 Widgets: `RewardKLTradeoff`, `KVCacheMeter`, `FeatureDictionary`.
- [ ] 5.2 Write L20, L21.
- [ ] 5.3 Write L22, L23.
- [ ] 5.4 Write L24 with the design-document rubric.
- [ ] 5.5 Remove the `--phase` flag; full validator must pass for all 24 lessons.

### Phase 6: Hardening and handoff
- [ ] 6.1 Full Playwright suite across a complete simulated learner path (L01 to L24 with solutions).
- [ ] 6.2 Accessibility and mobile pass (Lighthouse at least 90).
- [ ] 6.3 Content review pass: re-read every derivation; every numeric claim backed by a test or a derivation in the lesson.
- [ ] 6.4 Run all 10 acceptance criteria; fix until all pass.
- [ ] 6.5 Final README for the owner: the site URL, how to add the API key, how to open Colab lessons. Nothing else.

---

## 14. What to report to the owner

At the end of each phase, send one short message: the live URL, which lessons are now available, and anything you need from them (normally nothing). Do not send logs, diffs, or step-by-step narration.
