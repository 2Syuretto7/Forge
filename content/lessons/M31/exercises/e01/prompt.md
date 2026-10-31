# Hoeffding's inequality and sample sizes

For $n$ independent variables in $[a, b]$, the average misses its mean by at least $\varepsilon$ with probability at most $2e^{-2n\varepsilon^2/(b - a)^2}$ (Section 1). Read the other way: with probability at least $1 - \delta$ the miss is below $\varepsilon = (b - a)\sqrt{\ln(2/\delta)/(2n)}$.

- `hoeffding_bound(n, eps, a=0.0, b=1.0)`: the bound, capped at 1.
- `hoeffding_epsilon(n, delta, a=0.0, b=1.0)`: the guaranteed half-width.
- `hoeffding_n(eps, delta, a=0.0, b=1.0)`: the smallest $n$ that guarantees half-width $\varepsilon$ at confidence $1 - \delta$.

The tests answer the puzzle (1,000 test examples, $\delta = 0.05$: about $\pm 4.3$ points) and check the bound against simulated averages.

## Hints

1. Solve $2e^{-2n\varepsilon^2/(b - a)^2} = \delta$ for $\varepsilon$, or for $n$.
2. `math.ceil`, with a tiny rounding first.
3. The bound uses only the range, not the variance: it holds for every distribution on $[a, b]$, which is why it is pessimistic for a coin with $p$ near 0 or 1.
