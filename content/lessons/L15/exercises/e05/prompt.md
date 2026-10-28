# Fitting the parametric law

Gradient descent on Hoffmann's objective crawls along a long, flat valley. A better route uses the structure of the law: with the exponents fixed, $L = E + A N^{-\alpha} + B D^{-\beta}$ is **linear** in $(E, A, B)$, so they follow from a least-squares solve; only the two exponents need a search. `law` is provided.

1. `fit_for_exponents(alpha, beta, N, D, L)`: divide each run's equation $E + A N_i^{-\alpha} + B D_i^{-\beta} = L_i$ by $L_i$ (so every run counts by its relative error), solve by least squares, and return $E$, $A$, $B$ and the sum of squared relative errors.
2. `fit_parametric(N, D, L)`: try every $\alpha, \beta \in \{0.05, 0.07, \dots, 0.95\}$, then a grid ten times finer (step 0.002) within 0.02 of the best pair. Return a dictionary with keys `E, A, B, alpha, beta`.

## Hints

1. The design matrix has columns $1, N^{-\alpha}, D^{-\beta}$, each row divided by $L_i$; the target is a vector of ones.
2. `np.linalg.lstsq(X, target, rcond=None)[0]` solves it.
3. `np.arange(0.05, 0.951, 0.02)` gives the coarse grid.
