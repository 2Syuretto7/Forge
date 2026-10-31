# The union bound and the best of many models

Evaluate $k$ models on the same $n$ test examples. Each model's accuracy estimate is within $\varepsilon$ of the truth with probability $1 - \delta$; for all $k$ at once, the **union bound** charges $\delta$ once per model, so the half-width must grow to $\varepsilon_k = \sqrt{\ln(2k/\delta)/(2n)}$ (Section 2). Only logarithmically in $k$.

- `union_epsilon(n, k, delta)`.
- `best_of_random(k, n, rng)`: simulate $k$ classifiers that guess at random (each test example correct with probability $\frac12$, independently), and return the best test accuracy.
- `expected_excess(k, n, trials, rng)`: the average over `trials` of the best accuracy minus $\frac12$.

The tests show the best of 1,000 coin-flipping models scoring about 0.55 on 1,000 examples, below the union bound's $0.5 + \varepsilon_{1000}$, and the excess growing like $\sqrt{\ln k}$.

## Hints

1. `rng.random((k, n)) < 0.5`, then `.mean(axis=1).max()`.
2. A single model's 95 percent half-width at $n = 1000$ is $0.043$; for 1,000 models it is $0.073$.
3. The excess of the maximum of $k$ Gaussians grows like $\sqrt{2\ln k}$ standard deviations.
