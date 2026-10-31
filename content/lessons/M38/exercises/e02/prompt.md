# DPO, step 2: preferences as a likelihood

People compare two responses rather than score one. The **Bradley-Terry** model says the preferred response wins with probability $\sigma(r_w - r_l)$, depending only on the reward difference (Section 2), and a reward model is fitted by maximizing the log-likelihood $\sum\log\sigma(r_w - r_l)$ over observed pairs.

- `bt_prob(r, i, j)`: the probability that response $i$ beats $j$.
- `bt_loglik(r, pairs)`: the total log-likelihood of an array of `(winner, loser)` index pairs, computed stably as $-\sum\log(1 + e^{-(r_w - r_l)})$.
- `grad_bt_loglik(r, pairs)`.
- `count_matrix(pairs, K)`: $N_{ij}$, the number of times $i$ beat $j$, which is all the likelihood needs.

The tests run a **gradient check** and show that a constant added to every reward changes nothing.

## Hints

1. `np.logaddexp(0, -d)` is $\log(1 + e^{-d})$ without overflow.
2. The derivative of $\log\sigma(d)$ is $\sigma(-d)$; it adds to the winner's component and subtracts from the loser's.
3. Only differences enter: rewards from comparisons are defined up to a constant, exactly the freedom e01 found.
