# Angles in high dimension

- `random_cosines(d, n, seed=0)`: the cosine similarities of `n` pairs of independent random vectors in $d$ dimensions with standard normal coordinates (`np.random.default_rng(seed)`), as an array.
- `typical_cosine(d, n=4000)`: the standard deviation of those cosines.
- `fraction_nearly_perpendicular(d, tol, n=4000)`: the fraction of pairs with $|\cos t| < $ `tol`.

The tests confirm the puzzle: the typical cosine is close to $1/\sqrt{d}$, and in 1,000 dimensions almost every pair is within $5^\circ$ of perpendicular ($|\cos t| < 0.087$).

## Hints

1. Draw arrays of shape `(n, d)` for each side and compute the row-wise cosines.
2. `np.std`.
3. `np.mean(np.abs(c) < tol)`.
