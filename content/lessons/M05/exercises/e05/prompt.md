# Limits by epsilon and N

The definition of a limit is a recipe: given a tolerance $\varepsilon$, produce an $N$ after which every term is within $\varepsilon$.

- `last_outside(seq, L, eps, max_n)`: the largest $n \leq$ `max_n` (counting from $n = 1$) with $|$`seq(n)`$ - L| \geq \varepsilon$, or 0 if every term from $n = 1$ is within $\varepsilon$. Within the range checked, every later term is inside, so $N$ = this number works up to `max_n`.
- `geometric_N(r, eps)`: the smallest whole $n \geq 1$ with $r^n < \varepsilon$, for $0 < r < 1$, from the formula $n > \ln \varepsilon / \ln r$.
- `harmonic_N(eps)`: the smallest $n$ with $1/n < \varepsilon$.

## Hints

1. Loop $n$ from 1 to `max_n` and remember the last $n$ outside the band.
2. `math.floor(math.log(eps) / math.log(r)) + 1`, then step up while $r^n \geq \varepsilon$ to guard against rounding.
3. $1/n < \varepsilon$ means $n > 1/\varepsilon$.
