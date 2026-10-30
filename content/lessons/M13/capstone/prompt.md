# Capstone: a PageRank engine

The starter's `make_web(seed=0)` returns `(n, src, dst)`: 300 pages in three communities of 100. Two communities only link among themselves; the third links into both and holds the pages without links.

1. `pagerank(n, src, dst, d=0.85, tol=1e-10, start=None)`: return `(scores, steps, residuals)` by sparse power iteration (as in e10), where `residuals` is the sum of absolute changes at each step and `steps` its length. Start from `start` if given, otherwise from the uniform distribution.
2. `google_dense(n, src, dst, d=0.85)`: the dense Google matrix, for checking only.
3. `second_eigenvalue(G)`: the second largest absolute value among the eigenvalues of `G`.
4. `predicted_steps(lam2, tol, r0)`: steps for the first residual `r0` to fall below `tol` at rate $|\lambda_2|$.
5. `top(scores, k=10)`: the indices of the `k` best pages, best first.

Two closed communities make the link matrix have the eigenvalue 1 twice, so the Google matrix has $|\lambda_2| = d$ exactly. The tests require the top ten to match a dense eigenvector reference, $|\lambda_2|$ to equal $d$, and, starting from all probability on the last page, the residual to shrink by $|\lambda_2|$ per step and your step count to be within 20 percent of the prediction (the first residual also contains faster modes, which die out early).

Start from the uniform distribution and the count drops far below the prediction. That is not luck: with a uniform teleport, the uniform start has exactly zero component along the slow eigenvector, because both communities would absorb it in the same proportions as they absorb the stationary distribution. Any other start shows the full rate $d$.
