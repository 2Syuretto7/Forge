# Importance sampling

To estimate $\mathbb{E}_p[f(X)]$ with samples from a different density $q$, reweight: $\mathbb{E}_p[f] = \mathbb{E}_q[f\,w]$ with $w = p/q$ (Section 5).

- `normal_logpdf(x, mu=0.0, sigma=1.0)`: the Gaussian log-density, elementwise.
- `is_estimate(f, logp, logq, xs)`: given samples `xs` from $q$, return the estimate and its standard error, with weights $w = e^{\log p - \log q}$.
- `ess(w)`: the effective sample size $(\sum w)^2/\sum w^2$; it equals $n$ when all weights are equal and falls toward 1 when one weight dominates.

The tests estimate $P(Z > 3) \approx 0.00135$ for a standard normal $Z$ naively and with the proposal $N(3, 1)$, and require the importance sampler's standard error to be at least ten times smaller.

## Hints

1. `-0.5 * ((x - mu) / sigma) ** 2 - np.log(sigma * np.sqrt(2 * np.pi))`.
2. Work with log-weights; exponentiate only the difference.
3. The proposal puts half its samples in the region that matters, the naive sampler one in 740.
