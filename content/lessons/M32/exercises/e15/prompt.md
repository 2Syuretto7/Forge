# Break it: a chain that looks converged

A chain stuck in one peak of a two-peaked target has a smooth trace, a healthy acceptance rate and a respectable effective sample size. Nothing in one chain says it is wrong. Several chains from scattered starting points do: the **potential scale reduction** $\hat R$ compares the variance between chains with the variance within them (Section 7). With $m$ chains of length $n$, chain means $\bar x_j$, within-chain variance $W$ (the mean of the chains' sample variances) and between-chain variance $B = n\cdot\operatorname{Var}_j(\bar x_j)$,

$$
\hat R = \sqrt{\frac{\frac{n - 1}nW + \frac Bn}{W}} .
$$

- `r_hat(chains)`: for an array of shape `(m, n)`, with `ddof=1` variances.
- `run_chains(starts, sep, step, n, rng)`: one random-walk Metropolis chain per start on the provided two-peaked target; shape `(len(starts), n)`.
- `ess(x)`: as in e08.

The tests find $\hat R$ near 1 when the peaks overlap, far above 1 when they are 10 apart, while every stuck chain on its own has an effective sample size in the hundreds.

## Hints

1. $\hat R$ near 1 means the chains agree; the usual threshold is 1.01.
2. Start the chains at both peaks, alternating, so a stuck sampler cannot hide.
3. $\hat R$ can only reveal what the starting points expose: if every chain starts in the same peak, it reads 1.
