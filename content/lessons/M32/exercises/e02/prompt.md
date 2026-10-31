# Stationary distributions three ways

A stationary distribution satisfies $\pi P = \pi$: it is a left eigenvector of $P$ with eigenvalue 1 (M13), scaled to sum to 1 (Section 2). Find it three ways and check that they agree.

- `stationary_eig(P)`: the eigenvector of $P^\top$ whose eigenvalue is closest to 1, real part, normalized to sum 1.
- `stationary_power(P, tol=1e-13, max_iter=100000)`: start from the uniform distribution and multiply by $P$ until the largest change is below `tol`.
- `stationary_sim(P, n, rng, x0=0)`: the fraction of time a simulated path of $n$ steps spends in each state (reuse e01's sampler).
- `two_state(a, b)`: the closed form for $P = \begin{pmatrix} 1 - a & a \\ b & 1 - b \end{pmatrix}$.

The tests compare all three on a random five-state chain, and check `two_state` against the eigenvector.

## Hints

1. `np.linalg.eig(P.T)` returns eigenvalues and eigenvectors as columns; pick the column with `np.argmin(np.abs(vals - 1))`.
2. The eigenvector may come back negative or complex with zero imaginary part; take the real part and divide by its sum.
3. For two states, balance the flow: $\pi_0 a = \pi_1 b$.
