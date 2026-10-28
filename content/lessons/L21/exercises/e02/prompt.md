# Why baselines help

Implement `estimator_stats(theta, rewards, baseline)`: the exact mean and the total variance (summed over coordinates) of the single-sample estimator $(r_a - b)\,\text{score}(a)$, by enumerating the actions. `softmax` and `score` are provided.

The tests check that every baseline gives the same mean, and that the expected reward as baseline gives a much smaller variance than zero.

## Hints

1. Mean: $\sum_a p_a v_a$; variance: $\sum_a p_a \|v_a - \text{mean}\|^2$.
2. Rewards shifted by a constant change the variance without a baseline, but not with the mean-reward baseline.
3. In language-model RL the baseline is usually a learned value function or the mean reward of several samples for the same prompt.
