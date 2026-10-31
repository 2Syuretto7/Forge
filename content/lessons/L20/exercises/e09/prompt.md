# The evaluation stage

The evaluation stage reports every number with an interval over items (L19).

1. `pass_at_k(n, c, k)`: from $n$ sampled answers per problem, $c$ of them correct, the unbiased estimate of the chance that at least one of $k$ samples is correct, $1 - \binom{n-c}{k}/\binom{n}{k}$.
2. `mean_ci(scores, n_boot=2000, seed=0, level=0.95)`: the mean of per-item scores and a percentile bootstrap interval over items.

## Hints

1. $\binom{n-c}{k}/\binom{n}{k} = \prod_{i=n-c+1}^{n} (1 - k/i)$, which avoids huge binomial coefficients.
2. If fewer than $k$ answers are wrong, every set of $k$ contains a correct one.
3. Average pass@k over problems, then bootstrap over problems.
