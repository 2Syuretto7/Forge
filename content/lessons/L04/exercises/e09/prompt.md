# KL between Gaussians: closed form, Monte Carlo and gradient

Implement Section 3's Gaussian formula and check it two ways.

- `kl_gauss(mu1, s1, mu2, s2)`: $\mathrm{KL}(\mathcal N(\mu_1, s_1^2)\,\|\,\mathcal N(\mu_2, s_2^2))$ in nats, where `s1`, `s2` are standard deviations.
- `kl_gauss_mc(mu1, s1, mu2, s2, n, seed)`: the Monte Carlo estimate $\frac1n\sum_i[\log p(x_i) - \log q(x_i)]$ with $x_i \sim p$ drawn by `np.random.default_rng(seed).normal(mu1, s1, size=n)`.
- `grad_kl_mu1(mu1, s1, mu2, s2)`: $\partial\,\mathrm{KL}/\partial\mu_1$, which you derive from the formula.

## Hints

1. `np.log(s2 / s1) + (s1**2 + (mu1 - mu2)**2) / (2 * s2**2) - 0.5`.
2. The Gaussian log density is $-\tfrac12\log(2\pi s^2) - (x-\mu)^2/(2s^2)$.
3. Only one term of the formula depends on $\mu_1$.
