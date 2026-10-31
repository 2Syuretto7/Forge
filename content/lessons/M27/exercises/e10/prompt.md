# Break it: forward and reverse KL on a bimodal target

Fit a single Gaussian $q$ to a two-peaked target $p$ (an equal mixture of $\mathcal N(-2, 0.6^2)$ and $\mathcal N(2, 0.6^2)$) in the two directions of Section 3, on a fine grid `x` with spacing `dx`.

- `mixture(x)`: the target density on the grid.
- `gauss(x, mu, s)`: a Gaussian density.
- `forward_kl_fit(x, p, dx)`: minimizing $\mathrm{KL}(p\|q)$ over Gaussians matches moments, so return the mean and standard deviation of $p$: $\mu = \sum p\,x\,dx$, $s = \sqrt{\sum p\,(x - \mu)^2\,dx}$.
- `reverse_kl(x, p, mu, s, dx)`: $\sum q \log(q/p)\,dx$ for $q = \mathcal N(\mu, s^2)$, skipping grid points where $q$ underflows to 0.
- `reverse_kl_fit(x, p, dx, mus, sigmas)`: grid search over the candidate arrays; return the best `(mu, s)`.

Expect the forward fit to sit between the peaks with a wide spread (mass-covering) and the reverse fit to sit on one peak with about the peak's own width (mode-seeking).

## Hints

1. Moment matching is the closed-form minimizer of the forward KL within the Gaussian family.
2. Mask `q > 0` before taking `log(q / p)`.
3. Loop over all `(mu, s)` pairs and keep the smallest reverse KL.
