# The sigmoid and the logit

- `sigmoid(x)`: $1/(1 + e^{-x})$, computed so that it never overflows: for $x \geq 0$ use the formula as written; for $x < 0$ use the equal form $e^{x}/(1 + e^{x})$, which only exponentiates a negative number.
- `logit(p)`: the inverse, $\ln(p/(1 - p))$ for $0 < p < 1$.
- `sigmoid_derivative(x)`: $\sigma(x)(1 - \sigma(x))$, the slope of the sigmoid (M15 derives it).

The tests check an **invariant**: $\sigma(-x) = 1 - \sigma(x)$ and $\operatorname{logit}(\sigma(x)) = x$ for many random $x$, and that $\sigma(\pm 1000)$ returns 1 and 0 without overflowing.

## Hints

1. `if x >= 0: return 1 / (1 + math.exp(-x))`.
2. Multiply the top and bottom of $1/(1 + e^{-x})$ by $e^x$ to get the second form.
3. `math.log(p / (1 - p))`.
