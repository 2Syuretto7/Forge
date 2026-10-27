# Counting linear pieces

A one-hidden-layer ReLU network with scalar input computes a piecewise linear function with at most one kink per unit. Count the pieces numerically.

- `count_pieces(w, b, a, lo, hi, n)`: evaluate $f(x) = \sum_j a_j \max(0, w_j x + b_j)$ on `n` evenly spaced points in `[lo, hi]` and compute the slope between consecutive points. A kink that falls strictly between two grid points produces one short segment with an intermediate slope, so two consecutive slope changes belong to the same kink. Return 1 plus the number of kinks found this way, treating slopes within `1e-6` as equal.
- `kink_locations(w, b, lo, hi)`: the sorted points $-b_j/w_j$ (for $w_j \neq 0$) that fall strictly inside `(lo, hi)`.

The tests check that random networks with $k$ units have at most $k + 1$ pieces, and exactly $k + 1$ when all kinks are distinct, inside the interval, and have nonzero output weights.

## Hints

1. `s = np.diff(f) / np.diff(x)`.
2. Mark changes with `np.abs(np.diff(s)) > 1e-6`, then count clusters: a change that immediately follows another change does not start a new kink.
3. A grid of 20,001 points resolves kinks that are not too close together; the tests keep them apart.
