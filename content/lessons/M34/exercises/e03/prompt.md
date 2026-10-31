# The variance of a dot product

Attention scores are dot products $q\cdot k$ of a query and a key with $d$ entries each. If the entries are independent with mean 0 and variance 1, then $\operatorname{Var}(q\cdot k) = d$: the scores grow like $\sqrt d$, and dividing by $\sqrt d$ restores variance 1 (Section 3).

- `dot_products(d, n, rng)`: $n$ dot products of independent standard normal vectors in $d$ dimensions.
- `score_variance(d, n, rng, scaled)`: the sample variance of the dot products, divided by $d$ first when `scaled` is true (that is, the scores $q\cdot k/\sqrt d$).
- `variance_ratio(ds, n, rng)`: the list of unscaled variances divided by $d$.

The tests confirm that the unscaled variance is $d$ for every width from 16 to 1,024, and that the scaled variance stays at 1.

## Hints

1. Each term $q_ik_i$ has mean 0 and variance $\mathbb{E}q_i^2\,\mathbb{E}k_i^2 = 1$; independent terms add variances.
2. `np.var` uses `ddof=0`, which is fine at these sample sizes.
3. Scaling by $1/\sqrt d$ divides the variance by $d$.
