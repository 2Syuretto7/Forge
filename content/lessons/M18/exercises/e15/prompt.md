# Gradient checks at a kink

$f(x) = \sum_i \max(0, x_i)$ has the gradient $\mathbb{1}[x_i > 0]$ everywhere except where some $x_i = 0$.

- `relu_sum(x)` and `relu_sum_grad(x)`.
- `check_at(x, h=1e-6)`: the relative error of a central-difference check at `x`.
- `safe_point(x, h=1e-6)`: a copy of `x` in which every entry closer than $10h$ to 0 is moved to $\pm 10h$ (keeping its sign, $+$ for exactly 0).

Inputs with an entry within $h$ of zero make the central difference straddle the kink and the check fail, although the gradient code is right. Choosing check points away from kinks, or jittering them, is part of writing a correct check.

## Hints

1. `(x > 0).astype(float)`.
2. A central difference straddling 0 gives $1/2$ for that entry.
3. `np.where(np.abs(x) < 10 * h, np.where(x < 0, -10 * h, 10 * h), x)`.
