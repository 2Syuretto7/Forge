# The KL-regularized optimum

Replace the entropy by a KL penalty toward a reference distribution $\pi$: maximize $\sum_i p_i r_i - \beta\,\mathrm{KL}(p\,\|\,\pi)$. The same Lagrange argument gives $p_i \propto \pi_i e^{r_i/\beta}$: the reference, reweighted by exponentiated rewards (Section 6). This is the target of RLHF, and DPO (L17) inverts it: from the optimal and reference distributions, the reward is recovered up to a constant, $r_i = \beta\log(p_i/\pi_i) + \text{const}$.

- `kl_optimum(pi, r, beta)`: stably, in log space.
- `kl_objective(p, pi, r, beta)`.
- `implied_reward(p, pi, beta)`: $\beta\log(p_i/\pi_i)$.

The tests run a **gradient check** of the objective's stationarity condition along the simplex, compare with random distributions, and recover the rewards from the optimum.

## Hints

1. `logits = np.log(pi) + r / beta`, then a stable softmax.
2. $\mathrm{KL}(p\|\pi) = \sum p_i\log(p_i/\pi_i)$.
3. The recovered reward differs from $r$ by the same constant in every coordinate: compare differences, or subtract the means.
