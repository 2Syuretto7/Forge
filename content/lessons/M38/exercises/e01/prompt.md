# DPO, step 1: the reward hidden in a policy

The DPO paper starts from the KL-regularized objective of M36, $\max_\pi\mathbb{E}_\pi[r] - \beta\,\mathrm{KL}(\pi\,\|\,\pi_{\text{ref}})$, whose optimum is $\pi^*(y) = \pi_{\text{ref}}(y)e^{r(y)/\beta}/Z$ (M30). Read backwards, the optimum determines the reward up to a constant (Section 2):

$$
r(y) = \beta\log\frac{\pi^*(y)}{\pi_{\text{ref}}(y)} + \beta\log Z .
$$

- `kl_optimal(ref_logp, r, beta)`: the log-probabilities of $\pi^*$ over $K$ responses, given the reference log-probabilities.
- `implied_reward(logp, ref_logp, beta)`: $\beta(\log\pi - \log\pi_{\text{ref}})$, the reward up to a constant.
- `same_up_to_constant(a, b, tol=1e-9)`: whether $a - b$ is constant.

The tests confirm that the implied reward of the optimal policy is the true reward plus a constant, for any reference policy.

## Hints

1. Normalize with log-sum-exp: $\log\pi^* = \log\pi_{\text{ref}} + r/\beta - \log\sum\exp(\cdot)$.
2. The constant $\beta\log Z$ is the same for every response, so differences of rewards are recovered exactly.
3. This is the step that lets DPO skip the reward model: a policy *is* a reward model, up to a constant.
