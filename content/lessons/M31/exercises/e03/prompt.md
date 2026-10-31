# Chernoff's bound, by optimizing a moment generating function

Markov's inequality applied to $e^{tS}$, for any $t > 0$, gives $P(\bar X \ge a) \le e^{-n[ta - \log M(t)]}$, where $M(t) = 1 - p + pe^t$ is a coin's MGF (M24). Choosing the best $t$ gives the **Chernoff bound**, whose exponent is the KL divergence between coins (M27): $\sup_t[ta - \log M(t)] = \mathrm{KL}(a\,\|\,p) = a\log\frac ap + (1 - a)\log\frac{1 - a}{1 - p}$ (Section 1).

- `log_mgf(t, p)` and `d_log_mgf(t, p)` $= \frac{pe^t}{1 - p + pe^t}$.
- `chernoff_exponent(a, p)`: maximize $ta - \log M(t)$ over $t \ge 0$ by bisection on its derivative $a - $ `d_log_mgf`, which decreases in $t$.
- `kl_bernoulli(a, p)`.
- `chernoff_bound(n, a, p)`: $e^{-n\cdot\text{exponent}}$, for $a > p$.

The tests run a **gradient check** of `d_log_mgf`, confirm the exponent is the KL divergence, and that the Chernoff bound sits between the exact one-sided tail and Hoeffding's one-sided bound $e^{-2n(a - p)^2}$.

## Hints

1. The derivative is positive at $t = 0$ (it equals $a - p$) and becomes negative for large $t$: bracket the root on $[0, 50]$.
2. Pinsker's inequality, $\mathrm{KL}(a\|p) \ge 2(a - p)^2$, is why Chernoff is never worse than Hoeffding.
3. The exact one-sided tail is $\sum_{k \ge na}\binom nk p^k(1 - p)^{n - k}$.
