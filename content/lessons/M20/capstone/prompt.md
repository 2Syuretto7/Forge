# Capstone: a sampler toolkit

Each sampler maps uniform numbers in $(0, 1]$ to a target distribution. For each, write three functions:

1. Exponential with rate 2: `exp_map(u)`, its inverse `exp_inverse(y)`, and `exp_density(y)`.
2. Box-Muller: `bm_map(u)` for a pair `u = [u1, u2]`, `bm_inverse(xy)` (with $u_1 = e^{-r^2/2}$ and $u_2$ the angle over $2\pi$, taken in $[0, 1)$), and `bm_density(xy)`, the standard bivariate normal.
3. Uniform on the unit disc: `disc_map(u)` with $r = \sqrt{u_1}$, `disc_inverse(xy)` and `disc_density(xy)` $= 1/\pi$ inside.
4. Cauchy: `cauchy_map(u)` $= \tan(\pi(u - \frac12))$, `cauchy_inverse(y)` and `cauchy_density(y)`.
5. Correlated Gaussian with covariance `SIGMA` (in the starter): `corr_map(u)` $= L \cdot$ Box-Muller, `corr_inverse(xy)` and `corr_density(xy)`.

Then the two checks, for any of them:

- `cov_check(inverse, density, points)`: the largest relative difference between `density(y)` and $|\det J_{\text{inverse}}(y)|$ computed numerically at each point (the uniform density is 1, so the change-of-variables formula says they are equal).
- `hist_check_1d(samples, density, lo, hi, bins)` and `hist_check_2d(samples, density, box, bins)`: the largest relative deviation between observed and expected counts over bins expected to hold at least 2,000 samples (counting noise is about $1/\sqrt N$ for $N$ expected samples), where the expected count of a 2-D bin uses the density at a 3 by 3 grid of points inside it, and only bins whose four corners all have positive density count.

`report()` runs both checks on 200,000 samples of each sampler. The tests require every change-of-variables check below $10^{-6}$ and every histogram check below 0.1, and show that a density off by the Jacobian factor fails.
