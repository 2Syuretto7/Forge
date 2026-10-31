# Error against cost

How good is a randomized SVD at each rank, and what do oversampling and power iterations buy? Measure against the optimum: by Eckart-Young (M14) no rank-$k$ matrix is closer to $A$ in the Frobenius norm than the truncated SVD, whose error is $(\sum_{j > k}\sigma_j^2)^{1/2}$ (Section 5).

- `relative_errors(A, ks, p, q, rng)`: for each $k$, $\lVert A - U_k\Sigma_kV_k^\top\rVert_F / \lVert A\rVert_F$ for the randomized SVD (rebuild e08's).
- `optimal_errors(s, ks)`: the same ratio for the truncated SVD, from the singular values `s`.
- `matvecs(k, p, q)`: the number of products of $A$ or $A^\top$ with a vector the method uses, $(k + p)(2q + 2)$, counting the final projection $Q^\top A$ as $k + p$ products.
- `make_matrix(m, n, decay, rng)` is provided: an $m \times n$ matrix with singular values $1/j^{\text{decay}}$.

The tests run on a $3000 \times 300$ matrix: one power iteration brings the randomized SVD within 2 percent of optimal at every rank for a fast-decaying spectrum, and power iterations matter most when the spectrum decays slowly.

## Hints

1. The cost of the method is a fixed number of passes over $A$, each a matrix product with $k + p$ columns; a full SVD costs about $mn^2$ flops regardless of $k$.
2. Reuse one random matrix per call, or average a few calls when you want smooth curves.
3. Relative errors fall slowly for a slowly decaying spectrum even at the optimum: no method can beat Eckart-Young.
