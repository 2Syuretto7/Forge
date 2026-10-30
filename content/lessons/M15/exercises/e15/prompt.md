# A step too small to see

- `vanishing_step(x, h)`: whether `x + h == x` in floating point.
- `forward_at(f, x, h)`: the forward difference.
- `smallest_visible_step(x)`: the smallest power of ten $10^{-k}$ ($k$ an integer from 0 to 30) with `x + 10**-k != x`.
- `digits_correct(est, exact)`: $-\log_{10}$ of the relative error, capped at 16 (16 when exact).

The tests reproduce the prediction: the forward difference of $x^2$ at $10^8$ with $h = 10^{-9}$ is exactly 0, and at $x = 1$ with $h = 10^{-15}$ it has about one correct digit.

## Hints

1. Floats near $x$ are spaced about $\varepsilon|x|$ apart.
2. Loop `k` from 0 upward and keep the last step that is still visible.
3. `math.log10`.
