# The rank depends on the tolerance

`make_noisy(seed=0)` in the starter builds a $50 \times 30$ matrix of rank 5 and adds measurement noise of size about $10^{-6}$. The starter also provides `rank(A, tol)` from e05.

- `rank_sweep(A, tols)`: the list of ranks for the given tolerances.
- `pivots(A)`: the absolute values of all $\min(m, n)$ pivots of elimination with complete pivoting and no tolerance, in the order found (they tend to decrease, though not strictly).
- `gap_rank(p)`: the number of pivots before the largest drop: the $k$ from 1 to `len(p) - 1` that maximizes $p_{k-1} / p_k$ (counting from 0). Treat a pivot of exactly 0 as $10^{-300}$.
- `honest_tol(noise, shape)`: a tolerance just above what noise of the given size can produce in elimination: `10 * noise * sqrt(max(shape))`.

With tolerances from $10^{-14}$ to $10^{2}$, the sweep shows rank 30 (noise counted as information) up to the noise level, a plateau at 5, and 0 once the tolerance exceeds the data. The pivots show why: five large ones, then a cliff of five orders of magnitude.

## Hints

1. `[rank(A, t) for t in tols]`.
2. For the pivots, run the loop of `rank` to the end and record `abs(U[k, k])` after each swap.
3. `np.argmax(p[:-1] / p[1:]) + 1`.
