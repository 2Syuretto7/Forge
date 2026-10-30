# Storing and applying a factorization

- `storage(m, n, k)`: numbers stored by a rank-$k$ factorization $U_k \Sigma_k V_k^\top$: $k(m + n + 1)$.
- `matvec_cost(m, n, k=None)`: multiply-adds counted as 2 operations for $Ax$: $2mn$ for the full matrix, or $2k(m + n) + k$ through the factors (apply $V_k^\top$, scale, apply $U_k$).
- `break_even_rank(m, n)`: the largest $k$ for which the factors are cheaper to store than the matrix.
- `gram_flops(m, n)`: forming $X^\top X$ for an $m \times n$ matrix, using symmetry: $mn^2$.

## Hints

1. Integer arithmetic.
2. Solve $k(m + n + 1) < mn$ for $k$.
3. For $5000 \times 768$, forming the Gram matrix is about $3 \times 10^9$ operations.
