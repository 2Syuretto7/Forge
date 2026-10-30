# Stationary distributions

Columns of a transition matrix sum to 1: `P[i, j]` is the probability of moving from state `j` to state `i`.

- `transition_matrix(C)`: from a matrix of counts `C[i, j]` (moves from `j` to `i`), divide each column by its sum.
- `stationary_power(P, tol=1e-12, max_iter=100000)`: start from the uniform distribution and apply `P` until the change (sum of absolute differences) is below `tol`.
- `stationary_eig(P)`: the eigenvector of the eigenvalue nearest 1, made real and scaled to sum to 1.

The tests check an **invariant** on random chains with positive entries: both methods agree, the result sums to 1, and $P\pi = \pi$.

## Hints

1. `C / C.sum(axis=0, keepdims=True)`.
2. `lam, V = np.linalg.eig(P)`, then `k = np.argmin(np.abs(lam - 1))`.
3. `v = np.real(V[:, k]); v / v.sum()` also fixes the sign.
