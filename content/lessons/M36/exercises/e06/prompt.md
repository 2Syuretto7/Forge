# Markov decision processes and the Bellman equation

A **Markov decision process** has states, actions, transition probabilities $P(s' \mid s, a)$, rewards $R(s, a)$ and a discount $\gamma < 1$ (Section 5). A policy $\pi(a \mid s)$ turns it into a Markov chain (M32) with transition matrix $P_\pi(s, s') = \sum_a\pi(a \mid s)P(s' \mid s, a)$ and expected reward $R_\pi(s) = \sum_a\pi(a \mid s)R(s, a)$. The value $V^\pi(s)$, the expected discounted return from $s$, satisfies the **Bellman equation** $V^\pi = R_\pi + \gamma P_\pi V^\pi$, a linear system.

- `discounted_return(rewards, gamma)`: $\sum_tr_t\gamma^t$.
- `chain_of(P, R, pi)`: `(P_pi, R_pi)`, with `P` of shape `(A, S, S)`, `R` of shape `(S, A)` and `pi` of shape `(S, A)`.
- `policy_evaluation(P, R, pi, gamma)`: solve $(I - \gamma P_\pi)V = R_\pi$.
- `mc_value(P, R, pi, gamma, s0, episodes, horizon, rng)`: the average discounted return of simulated episodes from $s_0$, truncated at `horizon` steps.

The tests compare the linear solve with Monte Carlo returns on a small random MDP.

## Hints

1. `np.einsum("sa,ast->st", pi, P)` builds $P_\pi$. For the simulation, `rng.choice` with probabilities is slow inside a loop; draw uniforms in advance and search the cumulative sums with `bisect.bisect_right`.
2. Truncating at a horizon $H$ loses at most $\gamma^H\max\lvert R\rvert/(1 - \gamma)$.
3. Policy evaluation is the M32 chain with rewards attached: the discount plays the role of the eigenvalue gap, and $(I - \gamma P_\pi)$ is always invertible.
