# How fast a geometric series settles

The remainder after $n$ terms of $1 + r + r^2 + \dots$ is $\frac{1}{1 - r} - S_n = \frac{r^n}{1 - r}$.

- `remainder(r, n)`: that remainder, from the formula.
- `terms_needed(r, eps)`: the smallest $n$ with remainder below `eps`. Solve $r^n < \varepsilon(1 - r)$ with logarithms, then adjust by one step if rounding put you off.
- `work_ratio(r1, r2, eps)`: `terms_needed(r2, eps) / terms_needed(r1, eps)`.

The tests compare $r = 0.9$ with $r = 0.99$: moving the ratio ten times closer to 1 multiplies the work by about ten. M29 meets this law as the convergence rate of gradient descent.

## Hints

1. `r ** n / (1 - r)`.
2. $n > \ln(\varepsilon (1 - r)) / \ln r$.
3. Check the answer with `remainder` on both sides of it.
