# Value iteration on a gridworld

The optimal value function satisfies the **Bellman optimality equation** $V^*(s) = \max_a\big[R(s, a) + \gamma\sum_{s'}P(s' \mid s, a)V^*(s')\big]$. **Value iteration** applies the right-hand side repeatedly; it is a contraction with factor $\gamma$ in the maximum norm, so it converges from any start, and the greedy policy of $V^*$ is optimal (Section 5).

- `gridworld(n, slip=0.1)` is provided: an $n \times n$ grid, start in the top-left corner, an absorbing goal in the bottom-right, reward $-1$ per step, and moves that go in a random direction with probability `slip`.
- `bellman_backup(P, R, V, gamma)`: the $S \times A$ array $Q(s, a) = R(s, a) + \gamma\sum_{s'}P(s' \mid s, a)V(s')$.
- `value_iteration(P, R, gamma, tol=1e-10)`: `(V, greedy_policy, sweeps)`, stopping when the largest change is below `tol`.
- `greedy_as_matrix(policy, A)`: the deterministic policy as an $S \times A$ array of probabilities.

The tests check the Bellman optimality equation, that evaluating the greedy policy exactly gives back $V^*$, and that each sweep shrinks the error by at most the factor $\gamma$.

## Hints

1. `np.einsum("ast,t->sa", P, V)` computes the expected next value for every state and action.
2. With reward $-1$ per step and no slips, $-V^*(s)$ would be the discounted number of steps to the goal.
3. Measure the contraction as $\lVert V_{k+1} - V^*\rVert_\infty/\lVert V_k - V^*\rVert_\infty$.
