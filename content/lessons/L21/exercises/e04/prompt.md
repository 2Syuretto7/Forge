# Advantage estimation

In multi-step episodes, how much better than expected was each action? With a value estimate $V$, the TD error $\delta_t = r_t + \gamma V_{t+1} - V_t$ is a one-step answer; the return minus the value is the full-episode answer. Generalized advantage estimation mixes them:
$$
A_t = \sum_{k \ge 0} (\gamma\lambda)^k \delta_{t+k}.
$$

1. `gae(rewards, values, gamma, lam)`, where `values` has one more entry than `rewards` (the value after the last step, 0 at the end of an episode).
2. `returns(rewards, gamma)`.

## Hints

1. Run backwards: $A_t = \delta_t + \gamma\lambda A_{t+1}$.
2. $\lambda = 0$ gives the TD errors; $\lambda = 1$ gives returns minus values.
3. In RL for language models the episode is one response, and often only the last token gets a reward.
