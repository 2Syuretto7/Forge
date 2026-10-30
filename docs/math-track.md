# Forge Mathematics: Zero to Hero for ML and MLE

Oct 30, 2026 · @Arnav

## Summary

The track is 38 lessons and 428 hours, taking a learner from arithmetic and estimation to deriving and reproducing the mathematics of a current ML paper. At about 8 hours a week that is roughly 13 months, which is the intended pace: slow, steady, nothing skipped.

- **Fits Forge as it is built.** Every lesson uses the existing eight-movement player (recall, puzzle, derivation, build, scale, break it, Feynman, capstone), the existing directives, the review queue and the AI Feynman grader. Every lesson is 10 or 12 hours and exactly 50 percent theory, 50 percent practice by the validator's own counting.
- **A true graph, not a list.** Six strands (number and information, algebra and proof, linear algebra, calculus, probability, optimization) run through six stages. 120 new edges: 74 vertical prerequisites, 27 horizontal links between strands at the same stage, and 19 long-range edges that carry an idea years forward. The longest prerequisite chain is 13 lessons.
- **Runs the full height of the site.** The track no longer stops at Foundations. Math lessons sit beside the core, architecture, systems and LLM lessons at every stage and link to them horizontally (M29 beside L09, M34 beside L13, M35 beside L15, M36 beside L21).
- **Replaces L01 to L04.** Their material, exercises and capstones move into M12, M14, M15, M19, M24, M25 and M27, and their outgoing edges are re-pointed, so nothing already built is lost.

The graph was checked with the same rules as Forge's validator: vertical edges form a DAG and never point backwards in stage; horizontal edges stay within one stage and cross strands; every lesson has an inbound edge, an outbound edge and at least one horizontal or long-range edge.

## Pedagogy

Each Feynman habit is turned into a movement the learner must pass, so the method is enforced by the player rather than recommended in prose.

| Feynman habit | Where it lives | What the learner does |
| --- | --- | --- |
| Start from the phenomenon, name it last | m1 Puzzle | Meets a concrete surprise and commits a prediction before any definition is given. The term (eigenvector, entropy) is introduced only after the thing is seen. |
| Knowing the name is not knowing the thing | m2 Derivation | Derives every result from earlier ones in small fill-in steps. No formula is stated that the learner has not built. |
| Know several representations of the same idea | m2 Derivation | Each central result is derived two ways (dot product by coordinates and by the law of cosines; Gaussian integral by squaring and by polar change of variables). |
| What I cannot create, I do not understand | m3 Build | Implements the object from scratch in Python before any library is allowed; tests check values, shapes, invariants and gradients. |
| Estimate before you calculate | m1, m4 | Order-of-magnitude predictions open puzzles and every Scale movement; M01 makes estimation a skill in its own right. |
| You must not fool yourself | m5 Break it | Breaks the construction on purpose (overflow, wrong order, missing pivot) and predicts each failure before running it. |
| Explain it simply to find the gaps | m6 Feynman | Writes a plain-language explanation for a 12-year-old or a peer; the AI grader scores it against key points and returns the gaps, which feed back into review cards. |
| Keep a notebook of things you do not know | m0 Recall, reviews | Gaps from m6 and failed predictions become spaced-repetition cards that return in later lessons' recall movements. |

**Slow and steady, enforced.** Four gating rules keep the learner from racing ahead:

1. One lesson in progress at a time; a lesson unlocks only when every vertical prerequisite is complete and its Feynman block has passed.
2. The review queue comes first each session; a new movement opens only when due reviews are cleared.
3. A lesson closes only at 80 percent or better on its own review cards one week after completion, not on the day it was finished.
4. Sessions are about 90 minutes, a natural break between movements. A 12-hour lesson therefore spans about 8 sessions over 10 to 14 days.

**Rigour ladder.** Proof expectations rise with the stage. In Prelude, results are argued with pictures and checked by machine on many cases (M03 makes the gap between testing and proof explicit). In Foundations, every central theorem is stated and proved. From Learning onwards, proofs use inequalities and limits (convergence rates, Hoeffding, Johnson-Lindenstrauss).

## Lesson template

Every lesson uses one of two minute budgets, both exactly 50 percent theory and 50 percent practice under Forge's rule that a `both` movement counts half to each side.

| Movement | Mode | 10-hour lesson (min) | 12-hour lesson (min) |
| --- | --- | --- | --- |
| m0 Recall | theory | 25 | 30 |
| m1 Puzzle | theory | 40 | 45 |
| m2 Derivation | theory | 170 | 210 |
| m3 Build | practice | 150 | 170 |
| m4 Scale | practice | 60 | 80 |
| m5 Break it | both | 60 | 70 |
| m6 Feynman | theory | 35 | 40 |
| m7 Capstone | practice | 60 | 75 |
| **Theory / practice** |  | **300 / 300** | **360 / 360** |

**Minimum density per lesson.** These exceed the validator's floor so that no lesson is shallow:

- At least 5 `:::predict` blocks (one per puzzle, one per derivation, one in Break it).
- At least 4 `:::derivation` blocks with fill-in steps; each central theorem derived two ways.
- At least 2 `:::widget` blocks, one in m1 or m2 and one in m4 or m5.
- 14 to 16 exercises plus the capstone. From M15 onward at least 3 carry a `test_grad*` central-difference check; before M15, the equivalent is 3 `test_invariant*` checks (identities, conservation, round trips).
- One `:::feynman` block with 4 to 6 key points, plus one written proof graded with the concept rubric in Foundations and later.
- At least 2 `:::edge` chips into the lesson (from its reuses) and 2 out of it (to its hooks), placed at the exact paragraph where the connection is felt.
- 8 to 12 review cards: concept, derivation, prediction and kata kinds.

**One growing library.** Each capstone adds a module to a learner-owned package, `forge_math`. Later lessons import earlier modules instead of NumPy equivalents where possible (M25's bootstrap uses M24's Monte Carlo engine; M33's randomized SVD calls M14's SVD and M12's QR). The code itself becomes the graph, and a bug in an early module surfaces in a later lesson, which sends the learner back along the edge.

## The graph

The track is a grid: strands run across, stages run down, and Forge's own lessons sit in the right-hand column of each stage they share.

&#91;embedded content: math track · 6 strands x 6 stages · 38 lessons\]

Prerequisites run down a column or diagonally between columns; horizontal edges tie strands within one band (M19 to M27, M14 to M23); long-range edges skip bands, such as M07 to L13 or M01 to M35.

| Edge type | Count | Rule | Example |
| --- | --- | --- | --- |
| Vertical | 74 | Prerequisite; forms a DAG; never points to an earlier stage | M18 to M19: the multivariable chain rule becomes reverse-mode autodiff |
| Horizontal | 27 | Same stage, different strand or track | M12 to M25: least squares is maximum likelihood under Gaussian noise |
| Long-range | 19 | Different stages; an idea planted early returns later | M14 to L20: SVD returns as the low-rank update in LoRA |

**How past and future meet.** Each edge is used in both directions. Forward, it is a hook at the end of the earlier lesson and an edge chip at the paragraph where the idea will return. Backward, it is the later lesson's reuse, which seeds its Recall movement with review cards from the earlier one, and a retro-annotation that Forge writes into the earlier lesson once the later one is complete. A learner rereading M07 after L13 sees, beside the rotation derivation, a note that this is how rotary position embeddings work.

**Threads.** Eight objects recur so often that they work as long arcs of their own; each return adds one level of depth.

| Thread | Lessons, in order of return |
| --- | --- |
| Softmax | M06 defined, M19 Jacobian, M26 made stable, M27 cross-entropy gradient, M30 maximum-entropy optimum, M34 saturation and 1/sqrt(d), M36 policy, then L05, L13, L21 |
| The Gaussian | M17 integral, M20 n-dimensional normalizer, M22, M23 conditioning, M24 central limit, M25 MLE, M34 concentration, M37 diffusion |
| Least squares | M02 two unknowns, M12 projection, M14 pseudo-inverse, M25 likelihood, M35 nonlinear fits, L05 |
| Condition number | M02 near-singular systems, M11 pivoting, M14 singular values, M26 stability, M28 valley shape, M29 rate of descent, M33 preconditioning |
| Logarithm | M01 magnitudes, M06, M26 log-sum-exp, M27 nats and bits, M35 log-log fits, L14 perplexity |
| Eigenvectors | M13, M14, M18 Hessian, M23 covariance ellipses, M28, M29 momentum, M32 stationary distributions |
| Variance of sums | M22 initialization, M24 standard error, M31 Hoeffding, M34 random directions, M36 estimator variance, L10 |
| Rotation | M07 plane and complex numbers, M10 matrices, M14 SVD as rotate-stretch-rotate, L13 rotary embeddings |

## Stage 0: Prelude

Eight lessons, 80 hours, assume nothing beyond arithmetic and end with functions, logarithms, rotation, counting and proof: everything Foundations takes for granted.

### M01 Numbers, magnitudes and estimation

Number and information · 10 hours · the starting point · unlocks M02

Across: M06 (scientific notation is a logarithm in disguise); M08 (orders of magnitude meet the size of sample spaces).

Planted for the future: M35 (orders of magnitude return as compute budgets on log-log axes).

- **Puzzle:** How many floating-point operations does one forward pass of a 1-billion-parameter model take, to within a factor of 3, with no calculator? Commit a guess, then build the answer by counting multiply-adds per token.
- **Derive:** Integers to rationals to reals; place value and scientific notation; significant figures; ratios, rates and units as algebra on dimensions; Fermi decomposition and why errors in a product of factors partly cancel.
- **Build:** Python as a calculator; a units-aware quantity class that refuses to add metres to seconds; a Fermi-estimate worksheet engine that propagates low/high bounds.
- **Scale:** Estimate GPU-hours for a small pretraining run, then compare with a measured matmul throughput in the browser.
- **Break it:** Overflow an int in NumPy int32, lose cents in float money, and find the unit error in a deliberately wrong estimate.
- **Feynman:** Explain to a 12-year-old why multiplying ten rough guesses can still give a good answer.
- **Capstone:** A Fermi pack of 12 ML-flavoured estimates (dataset size, FLOPs, memory, cost) each with error bars, scored against computed truths: at least 10 within a factor of 3.
- **Widgets:** MagnitudeLadder

### M02 Algebra: the art of the unknown

Algebra and proof · 10 hours · builds on M01 · unlocks M03, M04, M11

Planted for the future: M12 (two equations in two unknowns return as the normal equations).

- **Puzzle:** A model's loss fell from 4.0 to 2.5 when the learning rate went from 0.1 to 0.3 and the batch doubled. Which unknown can you solve for, and which can you not? Name what is missing before touching symbols.
- **Derive:** Variables as names for numbers; the field rules and every manipulation as a consequence of them; linear equations, systems of two by substitution and elimination; inequalities and the sign flip; absolute value; quadratic formula by completing the square.
- **Build:** A tiny expression tree with evaluate and simplify; a two-variable linear solver; a checker that verifies a claimed algebra step by evaluating both sides at random points.
- **Scale:** Solve 10,000 random 2x2 systems and count how many are nearly singular; first sight of conditioning.
- **Break it:** Divide by an expression that can be zero, square both sides of an inequality, and watch the random-point checker catch the false step.
- **Feynman:** Explain why you may do the same thing to both sides of an equation, and when that rule secretly fails.
- **Capstone:** A step-checked algebra notebook: 15 multi-step manipulations, each step validated by the random-point checker, with the two planted errors found.
- **Widgets:** BalanceScale

### M03 Logic, sets and proof

Algebra and proof · 10 hours · builds on M02 · unlocks M05, M08

Planted for the future: M31 (quantifiers and proof by contradiction return in generalization bounds).

- **Puzzle:** The number n^2 + n + 41 is prime for n = 0, 1, 2, all the way to 39. Is it always true? Predict, then let the computer find n = 40. Testing is not proof.
- **Derive:** Propositions, connectives, truth tables; for-all and there-exists and how negation swaps them; sets, subsets, unions, products, functions as sets of pairs; direct proof, contrapositive, contradiction (irrationality of the square root of 2), counterexample.
- **Build:** Truth-table generator; set operations from scratch; a property-based counterexample hunter that searches for violations of a stated claim.
- **Scale:** Run the hunter over 50 classic claims, half false; record how many examples each falsehood needed before it broke.
- **Break it:** Prove a false theorem with a hidden division by zero and an induction with a broken base case; locate the exact faulty line.
- **Feynman:** Explain the difference between 'for every x there is a y' and 'there is a y for every x' using an everyday example.
- **Capstone:** A proof portfolio of 10 statements: each proved in writing (Feynman-graded rubric) and stress-tested by the counterexample hunter.
- **Widgets:** TruthTable

### M04 Functions and their graphs

Algebra and proof · 10 hours · builds on M02 · unlocks M05, M06, M07, M09

Planted for the future: L07 (sums of shifted ReLUs return as one-hidden-layer networks).

- **Puzzle:** Stack two ReLU-shaped pieces and you get a bump. How many pieces do you need to draw a smooth hill to within 0.01? Sketch before you compute.
- **Derive:** Function as a machine with domain and codomain; graphs; composition and its order; inverses and when they exist; linear, affine, quadratic, polynomial, rational, piecewise; transformations (shift, scale, reflect) as composition with affine maps.
- **Build:** A function-composition library with domain checks; numerical inverse by bisection; a piecewise-linear interpolator built only from ReLU pieces.
- **Scale:** Fit 1,000 points from a smooth curve with 10, 100, 1,000 ReLU pieces and measure the maximum error.
- **Break it:** Compose in the wrong order, invert a non-injective function, and evaluate outside the domain; make each fail loudly.
- **Feynman:** Explain why f(g(x)) and g(f(x)) are usually different, with a real-life pair of actions.
- **Capstone:** ReLU curve builder: approximate 5 target functions with sums of shifted ReLUs, meeting stated error budgets, with a written count of pieces used.
- **Widgets:** FunctionMachine

### M05 Sequences, series and induction

Calculus · 10 hours · builds on M03, M04 · unlocks M06, M08, M15

Planted for the future: M29 (geometric series return as linear convergence rates).

- **Puzzle:** Add 1 + 1/2 + 1/4 + ... forever: finite. Add 1 + 1/2 + 1/3 + ... forever: infinite. Predict which, then watch partial sums for a million terms.
- **Derive:** Sequences and their limits (informal, then epsilon-N); sigma notation and its algebra; arithmetic and geometric series in closed form; proof by induction; harmonic divergence by grouping; big-O growth of sums.
- **Build:** Partial-sum engine with exact fractions; induction checker that verifies base case and inductive step symbolically on polynomials; operation counter for nested loops.
- **Scale:** Time nested-loop algorithms at n = 10 to 10^6 and fit the exponent on log-log axes; it should match your sum.
- **Break it:** Sum a convergent series in float32 forwards and backwards and get different answers; rearrange an alternating series to change its sum.
- **Feynman:** Explain why an infinite sum can be finite, without using the word limit.
- **Capstone:** Cost model of 8 algorithms (including naive and blocked matrix multiply) derived as sums, proved by induction, verified by timing to within 20 percent of the predicted ratio.
- **Widgets:** SeriesStacker

### M06 Exponentials and logarithms

Algebra and proof · 10 hours · builds on M04, M05 · unlocks M15, M26, M27

Across: M01 (scientific notation is a logarithm in disguise); M07 (e to the i theta joins growth and rotation).

- **Puzzle:** A loss curve looks like a straight line on log-log axes and a curve on linear axes. What law is hiding? Predict the slope's meaning.
- **Derive:** Integer powers to rational to real exponents; e as the limit of compounding; exp and log as inverse functions; the log rules derived from the power rules; log scales; the sigmoid and softmax as exp-based functions; a first look at log-sum-exp.
- **Build:** Compute e three ways; logs from scratch by bisection on exp; a log-scale plotter; a softmax and a naive log-sum-exp.
- **Scale:** Softmax over 50,000 logits from a vocabulary-sized vector; watch exp overflow at logits near 89 in float32.
- **Break it:** Feed logits of 1000 to the naive softmax and get NaN; fix it by subtracting the maximum and prove the fix changes nothing mathematically.
- **Feynman:** Explain why a logarithm turns multiplication into addition, and why that is useful for probabilities.
- **Capstone:** Growth-law detector: given 6 datasets, classify each as linear, exponential or power law from log and log-log fits, and estimate its parameters.
- **Widgets:** LogScaler

### M07 Trigonometry, the plane and complex numbers

Linear algebra · 10 hours · builds on M04 · unlocks M09

Across: M06 (e to the i theta joins growth and rotation).

Planted for the future: L13 (planar rotations return as rotary position embeddings).

- **Puzzle:** Rotate a point by 30 degrees, then by 45. Is that the same as rotating by 75? Now do it with complex multiplication and see the angles add by themselves.
- **Derive:** Pythagoras by rearrangement; the unit circle; sine and cosine as coordinates; radians; angle-addition formulas; polar coordinates; complex numbers as points, multiplication as rotate-and-scale; Euler's formula e^(i theta) as a definition that keeps every rule working.
- **Build:** 2D rotation by trig and by complex multiply; polar conversion; a rotary position-encoding toy that rotates pairs of coordinates by position-dependent angles.
- **Scale:** Rotate a 1,000-point shape 10,000 times in small steps and measure drift; renormalize.
- **Break it:** Accumulate rotation error until the shape shrinks; mix degrees and radians and diagnose it from the output alone.
- **Feynman:** Explain why multiplying by i is a quarter turn.
- **Capstone:** Rotary toy: show that the dot product of two rotated vectors depends only on their position difference, proved and verified numerically for 1,000 pairs.
- **Widgets:** UnitCircle

### M08 Counting and chance

Probability · 10 hours · builds on M03, M05 · unlocks M21

Across: M01 (orders of magnitude meet the size of sample spaces).

Planted for the future: M31 (counting returns as the union bound and growth functions).

- **Puzzle:** In a room of 23 people, is a shared birthday more or less likely than not? Commit, then simulate 100,000 rooms.
- **Derive:** Product and sum rules of counting; permutations; combinations and binomial coefficients; Pascal's identity by a counting argument; binomial theorem; probability as favourable over possible for equally likely outcomes; complements; inclusion-exclusion.
- **Build:** Exact counters with fractions; a Monte Carlo simulator; binomial coefficients three ways (factorials, Pascal, multiplicative) compared for overflow.
- **Scale:** Count sampling configurations of a mini-batch from a dataset of 10^6; estimate collision rates of hashed IDs.
- **Break it:** Count ordered when the problem is unordered; compute 200 choose 100 with factorials and overflow.
- **Feynman:** Explain why the birthday collision happens so early, using pairs rather than people.
- **Capstone:** Exact-versus-simulated report for 10 probability puzzles, each agreeing within 3 standard errors, plus a hash-collision estimate for a dedup pipeline.
- **Widgets:** CountingTree

## Stage 1: Foundations

Twenty lessons, 228 hours, build the undergraduate core in four parallel strands (linear algebra, calculus, probability, numerics and information) that meet at convexity in M28. L05 to L09 open only once their math prerequisites here are complete.

### M09 Vectors and the dot product

Linear algebra · 10 hours · builds on M04, M07 · unlocks M10

Planted for the future: M34 (The dot product returns as near-orthogonality in high dimension).

- **Puzzle:** Two word vectors in 300 dimensions: how do you decide whether they mean similar things without looking at a single coordinate by name?
- **Derive:** Vectors as arrows and as lists; addition and scaling; length; the dot product two ways (coordinates and lengths times cosine) and why they agree (law of cosines); Cauchy-Schwarz; projection onto a line; norms L1, L2, L-infinity.
- **Build:** Vector class without NumPy, then the NumPy version; cosine similarity; nearest neighbours by brute force.
- **Scale:** Nearest-neighbour search over 100,000 embedding-like vectors; vectorize and measure the speedup.
- **Break it:** Compare unnormalized dot products and watch long vectors win; compute cosine of a zero vector.
- **Feynman:** Explain what a dot product measures, without a formula.
- **Capstone:** Semantic search toy over a provided embedding set: top-5 neighbours for 20 queries, with recall at least 0.9 against a reference.
- **Widgets:** VectorPlayground

### M10 Matrices as linear maps

Linear algebra · 10 hours · builds on M09 · unlocks M11, M18

Planted for the future: L13 (Matrix products are the whole of attention's compute).

- **Puzzle:** A 2x2 grid of numbers turns a square into a slanted parallelogram. Which numbers say where the corners go? Predict the image of (1,0) and (0,1).
- **Derive:** Linearity; a matrix is what it does to basis vectors; matrix-vector product as a combination of columns; composition is the matrix product (and why it is not commutative); identity, inverse, transpose; the determinant as signed area scaling; block matrices; batch matmul shapes.
- **Build:** Matmul three ways (dot products, column combinations, outer products) with shape tests; 2D graphics transform pipeline; determinant of 2x2 and 3x3.
- **Scale:** Batched matmul of shape (64, 512, 512) in NumPy; count FLOPs and compare with measured time.
- **Break it:** Multiply in the wrong order, transpose the wrong factor, broadcast silently across a mismatched axis.
- **Feynman:** Explain why AB is usually not BA, using two moves on a sheet of paper.
- **Capstone:** Transform studio: compose rotations, shears and scalings to hit 8 target shapes, with each matrix derived by hand and checked numerically.
- **Widgets:** MatrixTransform

### M11 Linear systems, elimination and rank

Linear algebra · 12 hours · builds on M10, M02 · unlocks M12

Across: M26 (Pivoting is a stability choice, not only an algebra step).

- **Puzzle:** Three sensors, three equations, and the solver says 'singular'. Two of the sensors were measuring the same thing. How could you have known from the numbers alone?
- **Derive:** Gaussian elimination as row operations; LU factorization; pivoting; column space, null space, rank; linear independence, basis, dimension; rank-nullity theorem with proof; when Ax = b has none, one or infinitely many solutions.
- **Build:** Elimination with partial pivoting; LU solver; rank by elimination with a tolerance; null-space basis.
- **Scale:** Solve 1000x1000 systems; compare your LU with numpy.linalg.solve for time and residual.
- **Break it:** Remove pivoting and destroy accuracy on a matrix with a tiny leading entry; pick the rank tolerance badly.
- **Feynman:** Explain what rank means in terms of information in the data.
- **Capstone:** A robust linear solver passing 40 tests (singular, near-singular, rectangular, permuted), reporting rank and a residual for each.
- **Widgets:** EliminationStepper

### M12 Orthogonality, projections and least squares

Linear algebra · 12 hours · builds on M11 · unlocks M13, L05

Across: M25 (Least squares is maximum likelihood under Gaussian noise); M22 (Variance is a squared length; covariance an inner product).

Returning from the past: M02 (Two equations in two unknowns return as the normal equations).

- **Puzzle:** Fifty noisy points, two parameters, no exact solution. What does 'best' line even mean? Predict which residuals the best line makes zero on average.
- **Derive:** Orthogonality and orthogonal complements; projection onto a subspace; normal equations from geometry and again from calculus-free algebra; Gram-Schmidt; QR; why the residual is orthogonal to every column.
- **Build:** Projection matrices; Gram-Schmidt classical and modified; least squares by normal equations and by QR; polynomial fitting.
- **Scale:** Fit polynomials of degree 1 to 20 on 10,000 points; watch normal equations lose digits while QR holds.
- **Break it:** Fit degree 15 with normal equations and get nonsense coefficients; diagnose the lost digits.
- **Feynman:** Explain why the shortest path from a point to a plane meets it at a right angle, and why that solves least squares.
- **Capstone:** Curve-fitting service: QR least squares with residual diagnostics on 6 datasets, beating the normal-equation baseline on the ill-conditioned ones.
- **Widgets:** ProjectionExplorer

### M13 Eigenvalues, eigenvectors and quadratic forms

Linear algebra · 12 hours · builds on M12 · unlocks M14, M23, M28, M32

Across: M18 (Hessian eigenvalues decide minimum, maximum or saddle).

Planted for the future: M32 (A stationary distribution is an eigenvector with eigenvalue 1); M29 (Eigenvalues of the Hessian set momentum's optimal value).

- **Puzzle:** Apply the same matrix to a random vector 50 times. The vector swings round and settles on one direction. Which one, and why?
- **Derive:** Invariant directions; characteristic polynomial; diagonalization and its failure; symmetric matrices and the spectral theorem with proof via orthogonality; power iteration and its rate; quadratic forms and positive definiteness; Markov stationary distributions as eigenvectors.
- **Build:** Power iteration and inverse iteration; eigen-decomposition checks; positive-definiteness test via Cholesky attempt; PageRank on a small web graph.
- **Scale:** PageRank on a 100,000-node sparse graph; measure convergence against the spectral gap.
- **Break it:** Power iteration on a matrix with two equal-magnitude eigenvalues; a non-diagonalizable shear.
- **Feynman:** Explain what an eigenvector is to someone who has never seen a matrix.
- **Capstone:** PageRank engine on a provided graph, matching a reference ranking with convergence rate predicted from the second eigenvalue.
- **Widgets:** EigenFlow

### M14 The singular value decomposition

Linear algebra · 12 hours · builds on M13 · unlocks M33, M34

Across: M23 (PCA is the eigen-decomposition of the covariance matrix).

Planted for the future: L20 (SVD returns as the low-rank update in LoRA).

- **Puzzle:** Two thousand 768-dimensional embeddings, yet three directions carry most of the variance. How do you find those directions and how many you need?
- **Derive:** SVD from the eigen-decomposition of A^T A; geometry: rotate, stretch, rotate; Eckart-Young theorem; low-rank approximation; PCA as SVD of centred data; pseudo-inverse; condition number as the ratio of extreme singular values.
- **Build:** SVD via eigen-decomposition and power deflation; PCA pipeline; low-rank image compression; pseudo-inverse least squares.
- **Scale:** Truncated SVD of a 5,000 x 768 matrix; plot explained variance and reconstruction error against rank.
- **Break it:** Forget to centre the data before PCA; compute condition numbers through A^T A and square them.
- **Feynman:** Explain why any linear map is a rotation, a stretch and another rotation.
- **Capstone:** PCA pipeline explaining 95 percent of the variance of a synthetic embedding set, with written interpretation of the top 3 components (migrated from L01).
- **Widgets:** MatrixTransform, SpectrumBars

### M15 Limits, continuity and the derivative

Calculus · 12 hours · builds on M05, M06 · unlocks M16, M17, M26

Across: M24 (Limits make the law of large numbers precise).

- **Puzzle:** Zoom in on a curve until it looks straight. What is the slope of that straight line, and what happens at a ReLU's corner where zooming never straightens it?
- **Derive:** Limits from epsilon-N to epsilon-delta; continuity; derivative as best local linear approximation; rules (sum, product, quotient, chain) each proved from the definition; derivatives of exp, log, sin; one-sided derivatives and subgradients.
- **Build:** Symbolic differentiator on expression trees; finite differences forward and central; derivative checker.
- **Scale:** Sweep step size h from 1e-1 to 1e-16 and plot error: truncation falls, rounding rises, minimum near the square root of machine epsilon.
- **Break it:** Differentiate at a kink, at a discontinuity, and with h = 1e-15; explain each failure.
- **Feynman:** Explain what a derivative is using a car's speedometer and nothing else.
- **Capstone:** Differentiator verified on 30 functions: symbolic result checked against central differences at the optimal step, with an error budget for each.
- **Widgets:** TangentZoom

### M16 Taylor series, extrema and Newton's method

Calculus · 12 hours · builds on M15 · unlocks M18, M25

Planted for the future: M29 (The second-order Taylor term returns as the step-size limit 2/L).

- **Puzzle:** Your calculator computes sin(0.1) with only additions and multiplications. How? Predict how many terms give 10 correct digits.
- **Derive:** Mean value theorem; Taylor polynomials with remainder; critical points and the second-derivative test; convexity in one dimension; Newton's method and its quadratic convergence; gradient descent in 1D and the step-size limit 2/L.
- **Build:** Taylor approximators with error bounds; bisection, Newton, secant, gradient descent; convergence-rate measurement.
- **Scale:** Solve 100,000 root problems vectorized; compare iteration counts by method.
- **Break it:** Newton from a bad start that cycles; gradient descent with step above 2/L that diverges; predict both.
- **Feynman:** Explain why Newton's method doubles the number of correct digits each step.
- **Capstone:** 1D optimizer suite with measured convergence orders (linear, superlinear, quadratic) matching theory within 10 percent.
- **Widgets:** TaylorBuilder

### M17 Integration and accumulation

Calculus · 12 hours · builds on M15 · unlocks M20, M22

Across: M24 (Monte Carlo is integration by sampling).

- **Puzzle:** A density curve over \[0, 1\] has area 1. What is the chance a sample lands in \[0.2, 0.3\]? Turn a probability question into an area question.
- **Derive:** Riemann sums; the definite integral; fundamental theorem of calculus with proof; substitution and integration by parts as reversed chain and product rules; improper integrals; the Gaussian integral by squaring it.
- **Build:** Riemann, trapezoid, Simpson; adaptive quadrature; normalizing constants of densities.
- **Scale:** Integrate 1,000 functions to 1e-8; count function evaluations by method.
- **Break it:** Integrate a function with a singularity naively; integrate a highly oscillatory function with too few points.
- **Feynman:** Explain why the area under a speed curve is the distance travelled.
- **Capstone:** Adaptive quadrature library hitting 1e-8 on 20 integrals, including the Gaussian and a Beta normalizer, with evaluation counts reported.
- **Widgets:** RiemannSum

### M18 Multivariable calculus: gradients, Jacobians, Hessians

Calculus · 12 hours · builds on M16, M10 · unlocks M19, M20, M28

Across: M13 (Hessian eigenvalues decide minimum, maximum or saddle).

- **Puzzle:** You stand on a foggy hillside and can only feel the slope under your feet. Which way is steepest, and how do you know without seeing the hill?
- **Derive:** Functions R^n to R^m; partial derivatives; the gradient as the direction of steepest ascent (proof via Cauchy-Schwarz); directional derivatives; the Jacobian as the best linear map; multivariable chain rule as Jacobian product; the Hessian and second-order Taylor.
- **Build:** Numerical gradients and Jacobians; gradient checks; contour plotter with gradient arrows; Hessian by finite differences.
- **Scale:** Gradients of functions in 10,000 dimensions; finite-difference cost versus analytic.
- **Break it:** A gradient check that passes in float32 for the wrong reason; a saddle that looks like a minimum along the axes.
- **Feynman:** Explain why the gradient is perpendicular to contour lines.
- **Capstone:** Gradient-check harness used on 25 vector functions, central differences in float64 at relative error below 1e-6.
- **Widgets:** GradientField

### M19 Matrix calculus and automatic differentiation

Calculus · 12 hours · builds on M18 · unlocks L07, L08

Across: M27 (The cross-entropy gradient through softmax is p minus y); M26 (Finite differences fail at tiny steps; autodiff does not).

- **Puzzle:** A function has one million inputs and one output. Computing its gradient by finite differences needs a million evaluations. Reverse mode needs about two. Why?
- **Derive:** Derivatives of matrix expressions; vector-Jacobian and Jacobian-vector products; computational graphs; forward mode with dual numbers; reverse mode; the matmul VJPs; the softmax Jacobian; the cost argument for reverse mode.
- **Build:** Dual-number forward mode; scalar reverse-mode engine with topological sort; VJPs for matmul, softmax, log.
- **Scale:** Differentiate a 20-layer composed function; compare cost of forward versus reverse mode as input dimension grows.
- **Break it:** Reuse a node twice and forget to accumulate gradients; get the topological order wrong.
- **Feynman:** Explain how reverse mode can get every partial derivative in one backward sweep.
- **Capstone:** Dual-number and reverse-mode library that differentiates a 20-line function, verified against finite differences (migrated from L03).
- **Widgets:** ComputationGraph

### M20 Multiple integrals and change of variables

Calculus · 10 hours · builds on M17, M18 · unlocks M23

Planted for the future: M37 (Change of variables returns as density transport in diffusion).

- **Puzzle:** Sample a point uniformly in a square and map it through a function. Where do the samples crowd? Predict the density before you plot.
- **Derive:** Double and triple integrals; Fubini; change of variables and the Jacobian determinant; polar and spherical coordinates; the Gaussian normalizer in n dimensions; densities under invertible maps.
- **Build:** Monte Carlo and grid integration in 2D; Box-Muller transform; density-transform checker by histogram.
- **Scale:** Volume of the unit ball from 2 to 50 dimensions by formula and by sampling; watch it vanish.
- **Break it:** Forget the absolute Jacobian determinant and get a density that does not integrate to 1.
- **Feynman:** Explain why stretching space thins out probability.
- **Capstone:** Sampler toolkit: 5 transforms from uniform noise to target densities, each verified by histogram and by the change-of-variables formula.
- **Widgets:** JacobianWarp

### M21 Probability spaces, conditioning and Bayes

Probability · 10 hours · builds on M08 · unlocks M22

Across: M27 (Surprise of an event is minus the log of its probability).

- **Puzzle:** A test is 99 percent accurate; the disease affects 1 in 1,000. You test positive. Commit to a probability that you are ill.
- **Derive:** Sample spaces, events, the axioms; conditional probability; independence; law of total probability; Bayes' rule by the area picture; base rates; conditional independence.
- **Build:** Event algebra on finite spaces; Bayes calculator; naive Bayes classifier from scratch with Laplace smoothing.
- **Scale:** Naive Bayes on a 20,000-document text set; calibration plot.
- **Break it:** Assume independence where there is none and get overconfident posteriors; zero counts without smoothing.
- **Feynman:** Explain why most positive tests for a rare disease are false alarms.
- **Capstone:** Naive Bayes filter at a stated accuracy with a reliability diagram and a written note on where independence fails.
- **Widgets:** BayesGrid

### M22 Random variables, expectation and variance

Probability · 12 hours · builds on M21, M17 · unlocks M23, M24, M27, M32

Across: M12 (Variance is a squared length; covariance an inner product).

- **Puzzle:** Initialize a weight as the sum of 512 small random numbers. How large is it typically? Commit to a number, then sample.
- **Derive:** Random variables as functions; PMF, PDF, CDF; expectation and its linearity; variance and covariance; variance of sums; Bernoulli, binomial, Poisson, uniform, exponential, Gaussian; inverse-CDF sampling.
- **Build:** Samplers for each distribution from uniforms; moment estimators; a goodness-of-fit check by CDF distance.
- **Scale:** Draw 10^7 samples per distribution; verify means and variances to the predicted precision.
- **Break it:** Sample a Cauchy variable and watch the sample mean refuse to settle; use variance of a sum without independence.
- **Feynman:** Explain why the variance of a sum of independent pieces adds, and what that says about initialization.
- **Capstone:** Distribution library of 8 samplers passing CDF-distance tests at 10^6 samples, plus the variance-preserving init scale derived and verified.
- **Widgets:** DistributionPlayground

### M23 Multivariate distributions and the Gaussian

Probability · 12 hours · builds on M22, M13, M20 · unlocks M37

Across: M14 (PCA is the eigen-decomposition of the covariance matrix).

- **Puzzle:** Height and weight are correlated. Given someone's height, how much does your uncertainty about weight shrink? Predict the shape of the cloud of points.
- **Derive:** Joint, marginal, conditional; covariance matrix as a positive semidefinite matrix; the multivariate Gaussian and its ellipses via the eigenvectors of the covariance; affine maps of Gaussians; conditioning a Gaussian (Schur complement); Cholesky sampling; whitening.
- **Build:** Multivariate Gaussian sampler and log-density; conditional Gaussian; whitening transform; 1D Kalman-style tracker.
- **Scale:** Fit a 256-dimensional Gaussian to embeddings; compare sample covariance quality with sample size.
- **Break it:** Covariance estimated from fewer samples than dimensions is singular; Cholesky of a not-quite-PSD matrix.
- **Feynman:** Explain why the contours of a 2D Gaussian are ellipses and what sets their axes.
- **Capstone:** Gaussian toolkit with conditioning and a tracker that follows a noisy target, beating raw measurements by a stated error margin.
- **Widgets:** GaussianEllipse

### M24 Limit theorems and Monte Carlo

Probability · 12 hours · builds on M22 · unlocks M25, M29, M31

Across: M15 (Limits make the law of large numbers precise); M17 (Monte Carlo is integration by sampling); M26 (Summing a million samples needs compensated summation).

Planted for the future: M36 (Monte Carlo returns as gradient estimation).

- **Puzzle:** Average 30 die rolls, many times over, and histogram the averages. Why is the result a bell curve when a die is flat?
- **Derive:** Markov and Chebyshev inequalities with proofs; weak law of large numbers; central limit theorem statement and a sketch via moment generating functions; Monte Carlo integration; standard error; importance sampling and its variance.
- **Build:** Monte Carlo estimators with confidence intervals; importance sampler; CLT simulator.
- **Scale:** Estimate a rare-event probability of 1e-6 naively and with importance sampling; compare samples needed.
- **Break it:** Importance sampling with a proposal lighter-tailed than the target; CLT on a heavy-tailed variable.
- **Feynman:** Explain why error bars shrink like one over the square root of the number of samples.
- **Capstone:** Monte Carlo engine reporting estimates with 95 percent intervals that cover the truth in at least 93 of 100 repeated runs.
- **Widgets:** CLTMachine

### M25 Inference: likelihood, MLE, MAP and the bootstrap

Probability · 12 hours · builds on M24, M16 · unlocks M31, M35, L05, L06

Across: M12 (Least squares is maximum likelihood under Gaussian noise); M27 (Maximizing likelihood is minimizing cross-entropy); M28 (Negative log-likelihoods of exponential families are convex).

Planted for the future: L23 (The bootstrap returns as confidence intervals on evals).

- **Puzzle:** A coin lands heads 7 times in 10. What is your best estimate of its bias, and how sure should you be? Two schools give two answers.
- **Derive:** Estimators, bias and variance; likelihood; MLE for Bernoulli, Gaussian, Poisson; Fisher information sketch; Bayesian posterior; conjugate priors; MAP as regularized MLE; the bootstrap; confidence versus credible intervals.
- **Build:** MLE solvers; Beta-Binomial posterior; bootstrap resampler; interval coverage checker.
- **Scale:** Bootstrap a metric over 100,000 examples with 2,000 resamples; vectorize.
- **Break it:** MLE that overfits with 3 data points; a bootstrap on dependent data.
- **Feynman:** Explain what the likelihood measures and why it is not a probability over the parameter.
- **Capstone:** A/B test analyzer with bootstrap and Bayesian posteriors, and a report on when they disagree (migrated from L02).
- **Widgets:** DistributionPlayground

### M26 Floating point and numerical stability

Number and information · 10 hours · builds on M06, M15 · unlocks M33

Across: M11 (Pivoting is a stability choice, not only an algebra step); M19 (Finite differences fail at tiny steps; autodiff does not); M24 (Summing a million samples needs compensated summation).

Planted for the future: L17 (Machine epsilon returns as the limits of bf16 and fp8).

- **Puzzle:** In float32, 16,777,216 + 1 = 16,777,216. Predict which ordinary-looking loss computation will silently suffer the same fate.
- **Derive:** Binary representation; sign, exponent, mantissa; rounding and machine epsilon; catastrophic cancellation; forward and backward error; condition number of a problem versus stability of an algorithm; stable log-sum-exp, softmax and log-sigmoid; compensated summation.
- **Build:** Float decoder; Kahan summation; stable softmax, log-softmax, logsumexp and softplus with tests at extreme inputs.
- **Scale:** Sum 10^8 numbers in float16, float32, float64, pairwise and Kahan; tabulate errors.
- **Break it:** Variance by the one-pass textbook formula on large-mean data; cross-entropy computed from probabilities instead of logits.
- **Feynman:** Explain why subtracting two nearly equal numbers destroys information.
- **Capstone:** Numerically hardened stats and loss library that survives an adversarial test suite of 40 extreme inputs.
- **Widgets:** FloatFormats

### M27 Information theory: entropy, cross-entropy, KL

Number and information · 10 hours · builds on M22, M06 · unlocks M30, M36, L06, L14

Across: M19 (The cross-entropy gradient through softmax is p minus y); M21 (Surprise of an event is minus the log of its probability); M25 (Maximizing likelihood is minimizing cross-entropy).

Planted for the future: L21 (KL divergence returns as the RLHF penalty).

- **Puzzle:** A language model reports a loss of 1.5. In what units, and what does 1.5 mean about guessing the next character?
- **Derive:** Surprisal; entropy; source coding intuition; cross-entropy; KL divergence and Gibbs' inequality via Jensen; mutual information; maximizing likelihood equals minimizing cross-entropy; perplexity.
- **Build:** Entropy estimators; Huffman coder; cross-entropy and KL with stable logs.
- **Scale:** Bits per character of a text corpus under unigram, bigram and trigram models.
- **Break it:** KL with a zero in the wrong distribution; entropy estimated from too few samples.
- **Feynman:** Explain why entropy is the average number of yes-or-no questions.
- **Capstone:** Compression experiment: Huffman-code a corpus and compare bits per character with entropy estimates (migrated from L04).
- **Widgets:** EntropyBars

### M28 Convexity and the geometry of optimization

Optimization · 12 hours · builds on M18, M13 · unlocks M29, M30, L09

Across: M25 (Negative log-likelihoods of exponential families are convex).

- **Puzzle:** Gradient descent zig-zags across a long narrow valley. Predict how the number of steps grows as the valley gets 10 times narrower.
- **Derive:** Convex sets and functions; first- and second-order conditions; Jensen's inequality; L-smoothness and strong convexity; condition number of a quadratic as the eigenvalue ratio of its Hessian; Lagrange multipliers for equality constraints.
- **Build:** Convexity tests; gradient descent on quadratics with chosen spectra; Lagrange-multiplier solver for small problems.
- **Scale:** Quadratics in 1,000 dimensions with condition numbers 10 to 10^5; iterations to tolerance.
- **Break it:** Step size above 2/L; a non-convex function where descent finds a bad local minimum.
- **Feynman:** Explain why convex problems have no bad local minima.
- **Capstone:** Optimization lab reproducing the predicted iteration count of gradient descent on 10 quadratics within 15 percent.
- **Widgets:** LossLandscape

## Stages 2 to 5: Learning to Frontier

Ten lessons, 120 hours, sit beside the core, architecture, systems and LLM lessons at the same stage, so each advanced idea is learned next to the place it is used.

### M29 Gradient methods: convergence, momentum and noise

Optimization · Learning stage · 12 hours · builds on M28, M24 · unlocks M35, M36

Across: L09 (Proved rates meet the practical optimizers); M32 (Constant-step SGD is a Markov chain with a stationary distribution).

Returning from the past: M05 (Geometric series return as linear convergence rates); M13 (Eigenvalues of the Hessian set momentum's optimal value); M16 (The second-order Taylor term returns as the step-size limit 2/L).

- **Puzzle:** Adding momentum makes a ball roll faster down a valley, yet sometimes overshoot. On a quadratic, what momentum value is exactly optimal?
- **Derive:** Convergence proofs for gradient descent on smooth convex and strongly convex functions; heavy-ball and Nesterov on quadratics via eigen-analysis; SGD as noisy gradient; the noise floor; step-size decay schedules and why they are needed; Adam's moment estimates and bias correction.
- **Build:** GD, heavy-ball, Nesterov, SGD, Adam from scratch; rate measurement by log-linear fits.
- **Scale:** Logistic regression on 10^6 rows with each optimizer; compare wall clock and final loss.
- **Break it:** Constant-step SGD that stalls at its noise floor; Adam without bias correction in the first steps.
- **Feynman:** Explain why noisy gradients force the step size down over time.
- **Capstone:** Optimizer zoo with measured convergence rates matching proved rates within 15 percent, plus Adam's bias correction derived and verified.
- **Widgets:** LossLandscape, ConvergenceRates

### M30 Constrained optimization, Lagrange duality and KKT

Optimization · Learning stage · 12 hours · builds on M28, M27 · unlocks M38

Across: L05 (Ridge regression is a Lagrangian with a norm constraint).

Planted for the future: L21 (The KL-regularized optimum returns as the basis of DPO).

- **Puzzle:** Among all distributions with a given expected reward, which has the highest entropy? Predict the shape and you have predicted softmax.
- **Derive:** Lagrangian; inequality constraints and KKT conditions; weak and strong duality; the support vector machine and its dual; projected gradient descent; entropy-regularized maximization yields softmax (Gibbs); KL-regularized optimum as reweighted reference.
- **Build:** Projected gradient; SVM via the dual with coordinate ascent; Gibbs-distribution solver with temperature.
- **Scale:** SVM on 50,000 points; compare primal and dual objectives as a duality-gap stopping rule.
- **Break it:** Violate complementary slackness and find the bug from KKT residuals; temperature to zero and to infinity.
- **Feynman:** Explain what a Lagrange multiplier is as the price of a constraint.
- **Capstone:** Dual SVM solver with KKT residual below 1e-4, plus a derivation and check that the KL-regularized optimum is reference times exp(reward / beta).
- **Widgets:** KKTGeometry

### M31 Concentration and generalization theory

Probability · Learning stage · 12 hours · builds on M24, M25 · unlocks M34

Across: L06 (Concentration bounds put numbers on the generalization gap).

Returning from the past: M03 (Quantifiers and proof by contradiction return in generalization bounds); M08 (Counting returns as the union bound and growth functions).

- **Puzzle:** A model gets 92 percent on 1,000 test examples. How far could the true accuracy be from 92, guaranteed, not just likely?
- **Derive:** Hoeffding's inequality with proof; union bound; finite-class generalization bound; growth functions and VC dimension sketch; Rademacher complexity intuition; bias-variance decomposition derived exactly for squared loss.
- **Build:** Bound calculators; empirical generalization-gap experiments; bias-variance decomposition by repeated sampling.
- **Scale:** Measure generalization gaps for 200 model sizes; compare with bounds.
- **Break it:** Reuse the test set for model selection 1,000 times and watch the bound silently fail.
- **Feynman:** Explain why checking many models against one test set makes the winner look better than it is.
- **Capstone:** Evaluation report with Hoeffding and bootstrap intervals and a demonstration of test-set reuse inflating accuracy by a measured amount.
- **Widgets:** ConcentrationMeter, BiasVarianceCurve

### M32 Markov chains and MCMC

Probability · Learning stage · 12 hours · builds on M22, M13 · unlocks M37

Across: M29 (Constant-step SGD is a Markov chain with a stationary distribution).

Returning from the past: M13 (A stationary distribution is an eigenvector with eigenvalue 1).

- **Puzzle:** Shuffle a deck by repeated riffles. How many shuffles until it is random? Predict, then measure.
- **Derive:** Markov property; transition matrices; stationary distributions; detailed balance; mixing and the spectral gap; Metropolis-Hastings derivation; Gibbs sampling; random walks and Brownian motion as a limit.
- **Build:** Chain simulator; stationary distribution by eigenvector and by simulation; Metropolis-Hastings; effective sample size.
- **Scale:** Sample a 50-dimensional posterior; tune proposals by acceptance rate.
- **Break it:** A chain that is not irreducible; a proposal step far too large or too small.
- **Feynman:** Explain why a random walk with the right acceptance rule ends up sampling the right distribution.
- **Capstone:** MCMC sampler for a provided posterior with diagnostics (trace, autocorrelation, effective sample size) matching a reference within tolerance.
- **Widgets:** MarkovChainSim

### M33 Numerical linear algebra at scale

Number and information · Models and GPUs stage · 12 hours · builds on M14, M26 · unlocks M38

Across: L11 (Arithmetic intensity places each kernel on the roofline); M34 (Randomized SVD works because random projections preserve geometry).

- **Puzzle:** A 4096 x 4096 matmul takes 137 billion floating-point operations. Why can a smart order of loops make it ten times faster with the same arithmetic?
- **Derive:** FLOP and byte counts; arithmetic intensity; blocked algorithms; conjugate gradient and Krylov subspaces; preconditioning; randomized range finders and randomized SVD with error bounds; sketching.
- **Build:** Blocked matmul; conjugate gradient; randomized SVD; arithmetic-intensity calculator.
- **Scale:** Randomized versus full SVD on 20,000 x 2,000 matrices; error against time.
- **Break it:** Conjugate gradient on a non-symmetric matrix; randomized SVD without oversampling on a slowly decaying spectrum.
- **Feynman:** Explain why moving data, not arithmetic, is usually the bottleneck.
- **Capstone:** Randomized SVD meeting a stated relative error at under one-fifth the time of full SVD, with a roofline placement of each kernel.
- **Widgets:** Roofline, SpectrumBars

### M34 High-dimensional geometry and random matrices

Linear algebra · Models and GPUs stage · 12 hours · builds on M31, M14 · unlocks M38

Across: L13 (Near-orthogonality explains the 1/sqrt(d) in attention); L10 (Variance preservation is what initialization and normalization protect); M33 (Randomized SVD works because random projections preserve geometry).

Returning from the past: M09 (The dot product returns as near-orthogonality in high dimension).

- **Puzzle:** Pick two random directions in 4,096 dimensions. Predict the angle between them, then sample a million pairs.
- **Derive:** Concentration of norms; near-orthogonality of random vectors; the Johnson-Lindenstrauss lemma with proof; why attention divides by the square root of d; variance-preserving initialization from first principles; Marchenko-Pastur spectrum; spectra of trained weights versus random.
- **Build:** JL projector; dot-product variance experiments; random-matrix spectrum estimator.
- **Scale:** Distance distortion of JL projections on 100,000 points across target dimensions.
- **Break it:** Attention scores without 1/sqrt(d) saturating softmax; initialization off by a factor of 2 compounding over 50 layers.
- **Feynman:** Explain why almost all random directions in high dimension are perpendicular.
- **Capstone:** JL compression of an embedding set preserving pairwise distances within 10 percent, plus a measured check of the 1/sqrt(d) and init-scale derivations.
- **Widgets:** RandomSpectrum

### M35 Power laws, nonlinear fitting and extrapolation

Probability · Scale stage · 12 hours · builds on M29, M25 · unlocks M38

Across: L15 (Your fitting machinery produces the scaling-law fit).

Returning from the past: M01 (Orders of magnitude return as compute budgets on log-log axes).

- **Puzzle:** Five small training runs fit a power law beautifully. How far may you extrapolate to a run 100 times larger before the error bars swallow the prediction?
- **Derive:** Power laws and scale invariance; log-log regression and its biases; nonlinear least squares; Gauss-Newton and Levenberg-Marquardt; uncertainty by bootstrap and by the Jacobian; extrapolation error growth; fitting L(N, D) = E + A/N^alpha + B/D^beta.
- **Build:** Gauss-Newton and Levenberg-Marquardt; bootstrap fit intervals; prediction bands.
- **Scale:** Fit a scaling law to 200 synthetic runs; compute the compute-optimal frontier.
- **Break it:** Log-log ordinary least squares on data with an irreducible loss floor; extrapolation far beyond the data.
- **Feynman:** Explain why a straight line on a log-log plot can still be a lie at larger scale.
- **Capstone:** Scaling-law fit with bootstrap intervals and a held-out larger run predicted within its interval.
- **Widgets:** ScalingFit

### M36 Score functions, gradient estimators and MDPs

Optimization · Frontier stage · 12 hours · builds on M29, M27 · unlocks M38

Across: L21 (REINFORCE is the policy-gradient estimator behind RLHF).

Returning from the past: M24 (Monte Carlo returns as gradient estimation).

- **Puzzle:** You cannot differentiate through a sampled token. How can you still get a gradient of the expected reward?
- **Derive:** The log-derivative trick; REINFORCE and its unbiasedness; baselines and variance reduction; the reparameterization trick; Gumbel-softmax; Markov decision processes, returns, value functions, Bellman equations; the policy gradient theorem.
- **Build:** Score-function and reparameterization estimators with measured variance; REINFORCE on a bandit and a small gridworld; value iteration.
- **Scale:** Variance of estimators across 10,000 samples as dimension grows.
- **Break it:** REINFORCE without a baseline on high-variance rewards; a biased baseline that depends on the action.
- **Feynman:** Explain how you can improve a choice you cannot differentiate by nudging the odds of the good outcomes.
- **Capstone:** Policy-gradient agent solving a gridworld, with variance of the gradient reduced by a measured factor using a learned baseline.
- **Widgets:** RewardKLTradeoff, EstimatorVariance

### M37 Stochastic differential equations and diffusion

Calculus · Frontier stage · 12 hours · builds on M32, M23 · unlocks M38

Returning from the past: M20 (Change of variables returns as density transport in diffusion).

- **Puzzle:** Add a little noise to an image a thousand times and you get static. Can you run the film backwards? What would you need to know at each frame?
- **Derive:** Brownian motion; stochastic differential equations; Euler-Maruyama; Ornstein-Uhlenbeck process and its stationary Gaussian; Ito's lemma intuition; score functions; denoising score matching; the reverse-time SDE.
- **Build:** Euler-Maruyama simulator; OU process; score estimation on a 2D mixture; a full 2D toy diffusion model in NumPy.
- **Scale:** Sampling quality against number of steps and noise schedule.
- **Break it:** Step size too large in Euler-Maruyama; a score network trained only at one noise level.
- **Feynman:** Explain how knowing which way density increases lets you turn noise back into data.
- **Capstone:** 2D diffusion model from scratch that turns Gaussian noise into a target mixture, scored by a distribution distance below a stated threshold.
- **Widgets:** DiffusionStepper

### M38 Capstone: the mathematics of a real paper

All strands · Frontier stage · 12 hours · builds on M30, M33, M34, M35, M36, M37 · final lesson of the track

Across: L24 (The paper audit method is applied to your capstone model).

- **Puzzle:** Pick one of three provided ML papers. Before reading its method section, predict which lessons of this track it will lean on.
- **Derive:** Re-derive every equation of the chosen paper (for example DPO from the KL-regularized objective, LoRA's low-rank argument, or Adam's update) step by step, flagging each lesson it draws on.
- **Build:** Reproduce the paper's core result in NumPy with tests, reusing your own forge\_math library rather than external packages.
- **Scale:** Run the reproduction at the largest size the browser or Colab allows; report where results diverge.
- **Break it:** Remove one assumption the derivation needs and show what fails, quantitatively.
- **Feynman:** Teach the paper's central idea in 5 minutes to a learner who has finished M15 but nothing after it.
- **Capstone:** A written derivation plus working reproduction, with a map of every lesson used and every edge it travelled.
- **Widgets:** ComputationGraph

## Integration with Forge

The track drops into the existing repo with two small schema changes, one validator change and 28 new widgets; everything else (player, directives, grader, reviews, Colab) is used as is.

### Migration of L01 to L04

| Old lesson | Material moves to | Capstone moves to | Old outgoing edges become |
| --- | --- | --- | --- |
| L01 Linear algebra as the geometry of data | M12 (projections, least squares, QR), M14 (SVD, PCA, conditioning) | M14 | M12 to L05; M28 to L09; M10 and M34 to L13; M14 to L20 |
| L02 Probability, likelihood and estimation | M22, M24 (CLT, Monte Carlo), M25 (MLE, MAP, bootstrap) | M25 | M25 to L05, L06 and L23; M22 to M27 |
| L03 Calculus, Jacobians and automatic differentiation | M15 (finite differences), M18 (Jacobians), M19 (VJPs, dual numbers) | M19 | M19 to L07 and L08; M19 to M27 replaces L03 to L04 |
| L04 Information theory: entropy, cross-entropy, KL | M27 whole | M27 | M27 to L06, L14 and L21 |

Existing exercises keep their folders and are renamed into the receiving lesson. Learner progress maps one to one: completing L01 marks M14 complete, L02 marks M25, L03 marks M19, L04 marks M27, with their prerequisites shown as optional review rather than locked.

### Schema and validator changes

1. Add `prelude` to `Stage` in `src/content/types.ts` and to `stages` in `graph.yaml`, before `foundations`.
2. Add an optional `strand` field to `LessonSummary` (`NUM`, `ALG`, `LIN`, `CAL`, `PRB`, `OPT`, `ALL`). The map lays math lessons out in strand sub-columns, which keeps 38 nodes readable.
3. Validator rule 6 (horizontal edges are same stage, across tracks) also accepts two math lessons when their strands differ.
4. Validator rule 4 (three `test_grad*` exercises) applies from M15 onward; M01 to M14 instead need three `test_invariant*` exercises.
5. The roots exempt from the inbound-edge rule change from L01 to L03 to M01 alone.
6. Gating in `src/store/derive.ts`: unlock on completed prerequisites plus a passed Feynman block, and hold new movements while due reviews remain (the slow-and-steady rules above).

The attached `math-track-graph.yaml` is the lesson and edge list ready to merge, and `forge-math-track-plan.yaml` is the full plan as data.

### New widgets

Each lesson names one signature widget; its second widget is reused from an earlier lesson (M12 also embeds VectorPlayground, M23 embeds EigenFlow), so widgets themselves carry vertical links. Ten existing widgets are reused: MatrixTransform, ComputationGraph, DistributionPlayground, FloatFormats, EntropyBars, LossLandscape, BiasVarianceCurve, Roofline, ScalingFit, RewardKLTradeoff.

| Stage | New widgets (lesson) |
| --- | --- |
| Prelude | MagnitudeLadder (M01), BalanceScale (M02), TruthTable (M03), FunctionMachine (M04), SeriesStacker (M05), LogScaler (M06), UnitCircle (M07), CountingTree (M08) |
| Foundations | VectorPlayground (M09), EliminationStepper (M11), ProjectionExplorer (M12), EigenFlow (M13), SpectrumBars (M14, M33), TangentZoom (M15), TaylorBuilder (M16), RiemannSum (M17), GradientField (M18), JacobianWarp (M20), BayesGrid (M21), GaussianEllipse (M23), CLTMachine (M24) |
| Learning to Frontier | ConvergenceRates (M29), KKTGeometry (M30), ConcentrationMeter (M31), MarkovChainSim (M32), RandomSpectrum (M34), EstimatorVariance (M36), DiffusionStepper (M37) |

### Build order

Authoring follows the graph so that every lesson's recall and edge chips can point at lessons that already exist.

1. Schema and validator changes; `graph.yaml` merged with L01 to L04 still present, so the build stays green.
2. Prelude, M01 to M08, with their eight widgets. The learner can start here while the rest is written.
3. Foundations linear algebra and calculus, M09 to M20; migrate L01 and L03 into M12, M14 and M19, then delete L01 and L03.
4. Foundations probability and numerics, M21 to M28; migrate L02 and L04 into M25 and M27, then delete them.
5. Learning stage, M29 to M32, with horizontal chips into L05, L06 and L09.
6. M33 to M37 beside their L-lesson partners; then M38 and the retro-annotations that every M lesson places into its predecessors.
