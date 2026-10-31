# Break it: correlated samples

The rule "error bar $= s/\sqrt n$" assumes independent samples. Samples from a Markov chain (M32) or a time series are correlated, and the rule underestimates the error. The starter's `ar1_chains(runs, n, rho, rng)` returns `runs` independent chains of length `n` of the process $x_t = \rho x_{t-1} + \sqrt{1 - \rho^2}\,\varepsilon_t$, each with mean 0 and variance 1, as rows.

- `naive_se(x)`: $s/\sqrt n$ for one chain.
- `batch_means_se(x, batches=50)`: split the chain into `batches` equal consecutive blocks, average each block, and return the standard deviation of the block averages (`ddof=1`) over $\sqrt{\text{batches}}$. Blocks much longer than the correlation time are nearly independent.
- `inflation(rho)`: the factor by which the true standard error exceeds the naive one, $\sqrt{(1 + \rho)/(1 - \rho)}$.

The tests show the naive intervals covering the true mean far less than 95 percent of the time at $\rho = 0.9$, and batch means restoring the coverage.

## Hints

1. `x.reshape(batches, -1).mean(axis=1)` when the length divides evenly.
2. At $\rho = 0.9$ the inflation is $\sqrt{19} \approx 4.4$: 100,000 correlated samples are worth about 5,000 independent ones.
3. Each block should be many times longer than $1/(1 - \rho)$ steps.
