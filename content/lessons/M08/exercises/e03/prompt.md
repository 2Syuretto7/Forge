# Binomial coefficients three ways

- `comb_factorial(n, k)`: $n!/(k!\,(n-k)!)$ with exact integers (use `//`).
- `comb_pascal(n, k)`: from Pascal's rule, by filling rows of the triangle up to row $n$; no multiplication or division needed.
- `comb_multiplicative(n, k)`: multiply and divide step by step, $\binom{n}{k} = \prod_{i=1}^{k} \frac{n - k + i}{i}$, keeping every intermediate an exact integer (multiply first, then divide by $i$).

All three return 0 when $k < 0$ or $k > n$. The tests check an **invariant**: the three agree for every $0 \leq k \leq n \leq 40$, and $\binom{n}{k} = \binom{n}{n-k}$.

## Hints

1. Write your own factorial or use `math.factorial`.
2. A row is built from the previous one: `[1] + [prev[i - 1] + prev[i] for i in range(1, len(prev))] + [1]`.
3. After multiplying by $n - k + i$, the running value is divisible by $i$, because it equals $\binom{n-k+i}{i}$ times $i$... check it with the tests rather than trusting this hint.
