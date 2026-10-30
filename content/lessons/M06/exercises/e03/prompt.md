# The exponential function

- `exp_series(x, terms=30)`: $\sum_{k=0}^{\text{terms} - 1} x^k / k!$, each term built from the previous one.
- `exp(x)`: an accurate $e^x$ for any $x$ between $-700$ and $700$. The series alone is accurate only for small $|x|$, so use **argument reduction**: pick $k$ with $|x / 2^k| \leq 1$, compute $y = $ `exp_series(x / 2 ** k)`, then square $y$ $k$ times, since $e^x = (e^{x/2^k})^{2^k}$.

The tests compare with `math.exp` and check an **invariant**: $e^a e^b = e^{a+b}$ for many random $a$, $b$.

## Hints

1. `term *= x / k` builds $x^k / k!$ from $x^{k-1}/(k-1)!$.
2. `k = 0` then `while abs(x) / 2 ** k > 1: k += 1`.
3. `for _ in range(k): y = y * y`.
