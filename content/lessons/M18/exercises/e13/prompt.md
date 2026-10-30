# A gradient check that lies in float32

- `check(f, grad, x, dtype, h, tol)`: cast `x` to `dtype`, compute central differences in that precision for every entry, and return `(passed, rel_error)` comparing with `grad(x)` (also cast).
- `float32_noise_floor(f, x, h)`: the relative error of a central difference of a **correct** gradient in float32: about $\varepsilon_{32}|f|/h$ relative to the gradient, with $\varepsilon_{32} \approx 1.2 \times 10^{-7}$.

The tests plant a bug of one part in a thousand. In float32 with step $10^{-3}$ and tolerance $10^{-2}$, the usual settings for float32, the buggy gradient passes; in float64 with step $10^{-6}$ and tolerance $10^{-6}$ it fails, while the correct gradient passes both.

## Hints

1. `x = np.asarray(x, dtype=dtype)`; `h = dtype(h)` keeps arithmetic in that precision.
2. Make sure `f` returns the same dtype: `np.float32` inputs give `np.float32` sums with NumPy.
3. A check is only as strict as its precision allows.
