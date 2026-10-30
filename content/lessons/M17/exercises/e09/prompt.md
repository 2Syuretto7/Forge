# The Gaussian integral, numerically

- `gauss_trapezoid(n, L=6.0)`: the trapezoid rule with `n` strips for $\int_{-L}^{L} e^{-x^2}\,dx$.
- `polar_inner(n, R=6.0)`: Simpson's rule with `n` strips for $\int_0^R e^{-r^2} r\,dr$, which should be $\frac12$ (up to $e^{-36}$).
- `squared_check(n)`: `gauss_trapezoid(n) ** 2` and `2 * math.pi * polar_inner(n)`, which should both be $\pi$.

A surprise: the plain trapezoid rule is extraordinarily accurate here, $10^{-13}$ with only 40 strips, far better than its $h^2$ error suggests. For smooth functions that decay to zero at both ends, the trapezoid rule's error is exponentially small; the $h^2$ formula's error terms all cancel.

## Hints

1. Vectorize with `np.linspace` and `np.exp`.
2. Simpson as in e02.
3. Compare with `math.sqrt(math.pi)`.
