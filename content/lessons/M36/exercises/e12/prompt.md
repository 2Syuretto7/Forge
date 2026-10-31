# Measuring the variance reduction

How much does a baseline help, measured rather than felt? Fix a policy, sample many episodes, compute the REINFORCE gradient estimate from each, and compare the spread of the estimates with and without the baseline (Section 3). Use the exact value function $V^\pi$ as the baseline, the best state-dependent choice in practice.

- `episode_gradient(theta, traj, gamma, V=None)`: $\sum_t(G_t - V(s_t))(e_{a_t} - \pi(\cdot \mid s_t))$ in the rows of the visited states, with $V = 0$ when `None`.
- `variance_reduction(P, R, theta, gamma, n, rng)`: sample `n` episodes under the policy, compute both estimates for each, and return `(var_without, var_with, mean_gap)`: the total variances (sum of per-entry variances) and the largest absolute difference between the two mean estimates.
- `gridworld`, `policy` and `run_episode` are provided.

The tests run 400 episodes on the $5 \times 5$ gridworld under the uniform policy and under a partly trained one: the variance falls by a factor of more than 3, and the two means agree within their noise.

## Hints

1. Both estimates use the same episodes, so the difference of the means isolates the baseline's effect.
2. Compute $V^\pi$ by solving the Bellman equation of e06.
3. The mean gap should be small compared with the square root of `var_without / n`.
