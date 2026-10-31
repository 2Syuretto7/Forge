# Noising a mixture

Run the forward process $dx = -x\,dt + \sqrt2\,dW$ from data $x_0$: by e02, $x_t = e^{-t}x_0 + \sqrt{1 - e^{-2t}}\,\varepsilon$ (Section 5). If the data are a Gaussian mixture, so is $x_t$: each component's mean shrinks by $e^{-t}$ and its variance becomes $s_k^2e^{-2t} + 1 - e^{-2t}$. As $t$ grows every component tends to $N(0, 1)$: the data are forgotten.

- `noise(x0, t, rng)`: samples of $x_t$ given samples $x_0$.
- `noised_params(w, m, s, t)`: `(w, m_t, s_t)` of the mixture at time $t$.
- `kl_to_standard_normal(m, v)`: $\mathrm{KL}(N(m, v)\,\|\,N(0, 1)) = \frac12(v + m^2 - 1 - \ln v)$, for a single Gaussian (M27).

The tests compare noised samples with `noised_params`, and confirm that for a single Gaussian the KL divergence to the standard normal decays like $e^{-2t}$.

## Hints

1. Sample the mixture first, then noise, then compare means and variances, or better, quantiles.
2. The mixture's overall mean is $\sum_kw_km_k$, and it shrinks by $e^{-t}$ exactly.
3. For large $t$, $\mathrm{KL} \approx \frac12m_0^2e^{-2t} + \frac14(s_0^2 - 1)^2e^{-4t}$: the mean is forgotten slowest.
