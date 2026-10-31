# Fitting a Gaussian to 256-dimensional embeddings

The starter's `make_embeddings(n, seed)` returns `n` vectors in 256 dimensions from a fixed Gaussian whose variances decay like $1/k$ along hidden directions: a stand-in for sentence embeddings. Fit a Gaussian and score it on held-out vectors.

- `fit(X)`: the maximum-likelihood mean and covariance (with $\frac1n$).
- `shrink(S, alpha)`: $(1 - \alpha)S + \alpha\,\frac{\operatorname{tr}S}{d}\,I$, a blend with a multiple of the identity.
- `heldout_loglik(X_train, X_test, alpha=0.0)`: fit on `X_train`, shrink, and return the average log-density of the rows of `X_test`, through the Cholesky factor as in e03.

The tests compare 300 and 10,000 training vectors: with 300 the unshrunk fit is far worse than with 10,000, and a modest `alpha` recovers most of the gap.

## Hints

1. The sample covariance of 300 vectors in 256 dimensions is invertible but has tiny eigenvalues in directions it barely saw; held-out points that move in those directions get very low density.
2. Shrinkage lifts every eigenvalue by at least $\alpha\operatorname{tr}S/d$.
3. Reuse your `logpdf` from e03, and the starter's `gram` (see e10) for $X_c^\top X_c$.
