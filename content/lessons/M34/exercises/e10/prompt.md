# Distortion at scale

How much does a random projection distort distances in practice, and how does that depend on the target dimension $k$? For a fixed difference vector, $\lVert R^\top x\rVert^2/\lVert x\rVert^2$ is $\chi^2_k/k$, with standard deviation $\sqrt{2/k}$, whatever the original dimension (Section 4). Measure it on 20,000 points.

- `sample_pairs(n, m, rng)`: `m` random pairs `(i, j)` with $i \ne j$, as two index arrays.
- `pair_distortions(X, pairs, k, rng)`: $\lVert R^\top(x_i - x_j)\rVert^2/\lVert x_i - x_j\rVert^2 - 1$ for each pair, projecting only the differences.
- `distortion_table(X, ks, m, rng)`: a dict from each $k$ to `(std, q99)`, the standard deviation of the distortions and the 99th percentile of their absolute values.

The tests run on 20,000 points in 128 dimensions with 5,000 pairs and find the spread tracking $\sqrt{2/k}$ for $k$ from 8 to 64.

## Hints

1. Project the $m$ difference vectors, an $m \times d$ array, rather than all $n$ points.
2. Resample `i` and `j` until they differ, or draw `j` as `(i + offset) % n` with a nonzero offset.
3. The 99th percentile sits near $2.6$ standard deviations for large $k$, a little more for small $k$, where $\chi^2_k$ is skewed. With one $R$ for all pairs, the spread across pairs matches the theory when the differences point in all directions, as they do here.
