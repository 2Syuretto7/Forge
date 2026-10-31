# Markov and Chebyshev

Implement the two inequalities of Section 1 and check them against samples.

- `markov_bound(mean, a)`: for a nonnegative variable, $P(X \ge a) \le \mathbb{E}X / a$, capped at 1.
- `chebyshev_bound(var, eps)`: $P(\lvert X - \mu\rvert \ge \varepsilon) \le \operatorname{Var}X/\varepsilon^2$, capped at 1.
- `tail_prob(samples, a)`: the fraction of samples at least `a`.
- `two_sided_prob(samples, mu, eps)`: the fraction with $\lvert x - \mu\rvert \ge \varepsilon$.

The tests check that the bounds hold on several distributions, and that Chebyshev's bound is exactly attained by a three-point distribution: no better bound can use the variance alone.

## Hints

1. `min(1.0, mean / a)`.
2. `np.mean(samples >= a)`.
3. The bounds are loose for most distributions: the exponential's $P(X \ge 5) = e^{-5} \approx 0.007$ against Markov's $0.2$.
