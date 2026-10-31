# Autocorrelation and effective sample size

Samples from a chain are correlated, so their average is noisier than an average of independent draws. If the lag-$k$ autocorrelation is $\rho_k$, the variance of the mean of $n$ samples is about $\frac{\sigma^2}n\left(1 + 2\sum_{k \ge 1}\rho_k\right)$, so the chain is worth $n_{\text{eff}} = n/(1 + 2\sum_k\rho_k)$ independent samples (Section 7).

- `autocorr(x, max_lag)`: $\rho_0, \dots, \rho_{\text{max\_lag}}$ by the FFT: subtract the mean, zero-pad to length $2n$, multiply the transform by its conjugate, transform back, divide by the lag-0 value.
- `ess(x)`: add the autocorrelations in consecutive pairs $(\rho_1 + \rho_2), (\rho_3 + \rho_4), \dots$, stopping before the first pair with a negative sum, and return $n/(1 + 2\cdot\text{sum})$.
- `mcse(x)`: the Monte Carlo standard error of the mean, $\operatorname{sd}(x)/\sqrt{n_{\text{eff}}}$.
- `ar1(phi, n, rng)`: $x_0 \sim N(0, 1)$, $x_t = \phi x_{t-1} + \sqrt{1 - \phi^2}\,z_t$, a chain with stationary variance 1 and $\rho_k = \phi^k$.

The tests compare your estimates with the exact answers for AR(1), $n_{\text{eff}} = n\frac{1 - \phi}{1 + \phi}$, and check that `mcse` predicts the spread of the means of many independent chains.

## Hints

1. `np.fft.rfft(x, 2 * n)` pads with zeros; the padding stops the circular correlation from wrapping around.
2. Far out, the estimated $\rho_k$ are noise; summing them all would ruin the estimate, which is why the sum stops.
3. For $\phi = 0.9$ a chain of $n$ steps is worth only $n/19$ independent samples.
