# How long to noise?

The reverse process starts from $N(0, 1)$, but the forward process only reaches it as $t \to \infty$: at a finite end time $T$ the noised data still remember a little of themselves, and that mismatch is never corrected (Section 7). Measure it: sample with the exact score of e05's mixture for end times from $0.25$ to $6$.

- `quality_vs_T(score, data, Ts, steps, rng)`: $W_1$ to the data for samples generated with each end time $T$, each with `steps` geometric steps.
- `prior_mismatch(w, m, s, T)`: the $W_1$ distance between the exact noised mixture at time $T$ and $N(0, 1)$, computed from 2,000 matching quantiles of each (compute the mixture's quantiles by inverting its CDF on a fine grid).

The tests find the error large for $T = 0.25$ and falling as $T$ grows, and the mismatch shrinking by a factor $e^{-1}$ per unit of time once $T$ is large.

## Hints

1. The mismatch shrinks like $e^{-T}$: the mean of the noised data is $e^{-T}$ times the data mean.
2. The mixture's CDF is a weighted sum of normal CDFs; `math.erf` gives them, or integrate the density numerically.
3. Larger $T$ costs steps: with a fixed number of steps, the steps get longer.
