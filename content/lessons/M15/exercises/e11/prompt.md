# A million derivatives at once

- `central_vec(f, x, h)`: central differences of a vectorized NumPy function `f` at every entry of the array `x`, with `h` a number or an array the shape of `x`.
- `max_rel_error(est, exact)`: $\max_i |e_i - x_i| / |x_i|$.
- `compare_steps(n=1_000_000)`: for $f = \log$ at `n` points spread log-uniformly over $[10^{-3}, 10^{3}]$ (`np.logspace`), return `(fixed, scaled)`: the largest relative error with the fixed step $h = 10^{-5}$ and with the scaled step $h = \varepsilon^{1/3}|x|$.

A fixed step is too large for $x = 10^{-3}$ (truncation) and fine elsewhere; the scaled one stays near $10^{-10}$ throughout.

## Hints

1. `(f(x + h) - f(x - h)) / (2 * h)` works elementwise.
2. `np.finfo(float).eps ** (1 / 3) * np.abs(x)`.
3. One call over a million points takes milliseconds.
