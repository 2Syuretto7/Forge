# PPO's clipped objective

PPO reuses samples from the previous policy for several updates, weighting each by $\rho = \pi_\theta / \pi_\text{old}$, and removes the incentive to move $\rho$ outside $[1 - \epsilon, 1 + \epsilon]$:
$$
L = \operatorname{mean}\bigl(\min(\rho A,\; \operatorname{clip}(\rho, 1 - \epsilon, 1 + \epsilon) A)\bigr).
$$

Implement `ppo_objective(logp, logp_old, adv, eps)`: the objective and its gradient with respect to `logp`.

## Hints

1. $\partial \rho / \partial \log \pi = \rho$.
2. Where the clipped term is the smaller, it is constant in $\theta$, and the gradient is zero.
3. Positive advantage: no gain beyond $\rho = 1 + \epsilon$. Negative advantage: no gain below $1 - \epsilon$.
