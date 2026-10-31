# Break it: a rank too small

If the update a task needs has more directions than the adapter's rank, no amount of training recovers them.

1. `target_update(d, rank, seed=0, decay=0.7)`: a $d \times d$ update with singular values $0.7^i$ for $i < \text{rank}$ and zero beyond, a decaying spectrum like that of real fine-tuning updates.
2. `error_by_rank(M, ranks)`: the relative error of the best rank-$r$ approximation for each $r$.

## Hints

1. Build the update from orthonormal $U$ and $V$ (`np.linalg.qr` of random matrices) and the chosen singular values.
2. The error falls as singular values are captured, and reaches zero at the true rank.
3. When a fine-tune plateaus well above its full fine-tuning loss, try a larger rank or more adapted layers before more steps.
