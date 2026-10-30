# Gradient descent in one dimension

- `gd(df, x0, eta, steps)`: the list of iterates of $x \leftarrow x - \eta f'(x)$, `x0` included.
- `step_limit(L)`: $2/L$.
- `predicted_factor(eta, L)`: $|1 - \eta L|$, the factor by which the distance to the minimum of $\frac{L}{2}x^2$ shrinks per step.
- `descent_bound(f, df, x, eta, L)`: `(actual, guaranteed)`: the actual decrease $f(x) - f(x - \eta f'(x))$ and the descent lemma's guarantee $\eta(1 - L\eta/2) f'(x)^2$.

The tests include a **gradient check** of the descent lemma: on $f = \log\cosh x$, whose curvature is at most $L = 1$, the actual decrease is never below the guarantee.

## Hints

1. Append each new iterate.
2. On $\frac{L}{2}x^2$ the factor is exact at every step.
3. $\frac{d}{dx}\log\cosh x = \tanh x$ and its second derivative $1 - \tanh^2 x \leq 1$.
