# The mean value point

- `mean_value_point(f, df, a, b, tol=1e-12)`: a point $c$ in $(a, b)$ with $f'(c) = (f(b) - f(a))/(b - a)$, found by bisection on $g(c) = f'(c) - \text{slope}$, assuming $g$ changes sign between $a$ and $b$ (true when $f'$ is monotone).
- `taylor_remainder_point(x)`: for $f = e^x$ around 0 with degree 1, the $\xi$ in Taylor's remainder, $e^x - 1 - x = \frac{e^\xi}{2}x^2$, solved for $\xi$ exactly.

## Hints

1. Reuse your bisection from e02, or write the loop again.
2. For $x^3$ on $[0, 2]$ the slope is 4 and $c = 2/\sqrt 3$.
3. $\xi = \ln\big(2(e^x - 1 - x)/x^2\big)$, which lies between 0 and $x$.
