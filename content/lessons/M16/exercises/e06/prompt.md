# Convexity from the second derivative

- `second_diff(f, x, h=1e-4)`: the central second difference $(f(x + h) - 2f(x) + f(x - h))/h^2$.
- `convex_on_grid(f, a, b, n=200, h=1e-4)`: whether `second_diff` is at least $-10^{-6}$ at `n` evenly spaced points of $[a, b]$.
- `chord_check(f, a, b, trials=500, seed=0)`: whether $f(tx + (1 - t)y) \leq t f(x) + (1 - t) f(y) + 10^{-12}$ for random $x, y \in [a, b]$ and $t \in [0, 1]$.

The tests include a **gradient check** of the second difference against exact second derivatives, and check that the two convexity tests agree.

## Hints

1. The second difference has error about $h^2 |f''''|/12$ and rounding about $4\varepsilon|f|/h^2$: $h = 10^{-4}$ balances them roughly.
2. `np.linspace(a, b, n)`.
3. $\sin$ is concave on $[0, \pi]$ and convex on $[\pi, 2\pi]$.
