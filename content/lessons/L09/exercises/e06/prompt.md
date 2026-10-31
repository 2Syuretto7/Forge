# Positions: equivariance and sinusoidal encodings

1. `sinusoidal(n, d, base=10000.0)`: the `(n, d)` table with $\text{PE}_{p, 2i} = \sin(p / \text{base}^{2i/d})$ and $\text{PE}_{p, 2i+1} = \cos(p / \text{base}^{2i/d})$.
2. `is_permutation_equivariant(f, X, perm)`: whether `f(X[perm])` equals `f(X)[perm]` to within `1e-9`.

Then check: attention without a mask is permutation-equivariant; adding sinusoidal encodings to the input before attention breaks it; and the causal mask also breaks it (it depends on order).

## Hints

1. Build the angles as an outer product of positions `(n, 1)` and frequencies `(1, d/2)`.
2. Fill even and odd columns with slices `0::2` and `1::2`.
3. `np.allclose(a, b, atol=1e-9)`.
