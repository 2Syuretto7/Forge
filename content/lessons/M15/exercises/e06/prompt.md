# The limits behind e^x, ln x and sin x

- `exp_quotient(h)`: $(e^h - 1)/h$, which tends to 1.
- `sin_quotient(h)`: $\sin(h)/h$, which tends to 1.
- `log_slope(x, h)`: $(\ln(x + h) - \ln x)/h$, which tends to $1/x$.
- `order_of_error(q, limit, h)`: the ratio $|q(h) - L| / |q(h/2) - L|$, about 2 for an error proportional to $h$ and about 4 for one proportional to $h^2$.

Evaluate `math.expm1(h) / h` as well as `(math.exp(h) - 1) / h` at $h = 10^{-12}$: the first is accurate, the second wrong in the fifth digit. `expm1` exists for exactly this cancellation.

## Hints

1. Use `math.exp`, `math.sin`, `math.log`.
2. `(e^h - 1)/h = 1 + h/2 + ...`, an error of order $h$.
3. `sin(h)/h = 1 - h^2/6 + ...`, an error of order $h^2$.
