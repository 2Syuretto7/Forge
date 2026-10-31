# Estimating entropy from samples

The **plug-in** estimator computes the entropy of the empirical distribution. It is biased low: a finite sample rarely shows the full spread of a distribution. The **Miller-Madow** correction adds $(K_{\text{obs}} - 1)/(2n)$ nats, where $K_{\text{obs}}$ is the number of distinct values observed in $n$ samples.

- `plugin_entropy(samples, K)`: entropy in nats of the empirical distribution of integer samples in $\{0,\dots,K-1\}$.
- `miller_madow(samples, K)`: the plug-in estimate plus the correction.
- `average_estimates(p, n, trials, seed)`: draw `trials` samples of size `n` from `p` with `np.random.default_rng(seed).choice(len(p), size=(trials, n), p=p)` and return the average `(plugin, miller_madow)` estimates.

The tests check that the plug-in estimate is biased low on small samples and that the correction removes most of the bias.

## Hints

1. `np.bincount(samples, minlength=K) / n`.
2. $K_{\text{obs}}$ is the number of nonzero counts.
3. Loop over the trials; each estimate is cheap.
