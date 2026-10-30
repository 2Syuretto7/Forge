# Goodness of fit by CDF distance

How do you test a sampler? Compare the empirical CDF of its samples, $F_n(x) = \frac{1}{n}\#\{i : x_i \le x\}$, with the CDF it should have. The largest gap, $D_n = \sup_x \lvert F_n(x) - F(x)\rvert$, is the **Kolmogorov-Smirnov distance**, and the Dvoretzky-Kiefer-Wolfowitz inequality bounds it for a correct sampler: $P(D_n > \varepsilon) \le 2e^{-2n\varepsilon^2}$.

- `ks_distance(samples, cdf)`: $D_n$ for a continuous `cdf` (a function of an array). With the samples sorted, $D_n = \max_i \max\big(\frac{i}{n} - F(x_{(i)}),\ F(x_{(i)}) - \frac{i - 1}{n}\big)$.
- `discrete_distance(samples, cdf_values)`: for integer samples, $\max_k \lvert F_n(k) - F(k)\rvert$ over $k = 0, \dots, K - 1$, where `cdf_values[k]` $= F(k)$.
- `dkw_threshold(n, alpha)`: the $\varepsilon$ with $2e^{-2n\varepsilon^2} = \alpha$. A correct sampler exceeds it with probability at most `alpha`.

The tests accept correct samplers at $10^6$ samples and reject a Gaussian shifted by 0.02 and a Poisson with the wrong rate.

## Hints

1. $\varepsilon = \sqrt{\log(2/\alpha)/(2n)}$, about $1.36/\sqrt n$ at $\alpha = 0.05$.
2. `np.bincount(samples, minlength=K)[:K]`, then `np.cumsum` divided by $n$.
3. The threshold shrinks like $1/\sqrt n$: a million samples detect a shift of a few thousandths of a standard deviation.
