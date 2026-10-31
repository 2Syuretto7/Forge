# Scale: 50,000 points, a million actions, 100,000 channels

::::predict{id=p4 kind=choice answer=a}
A solver reports a primal value $P(w) = 10.000$ and a dual value $D(\alpha) = 9.999$ for an SVM. What do you know about the true optimum $P^\star$?

- $9.999 \le P^\star \le 10.000$: the current $w$ is within $10^{-4}$ of optimal, relatively.
- Nothing until the solver converges.
- $P^\star = 9.9995$, the midpoint.
- $P^\star \ge 10$.

:::reveal
Weak duality traps the optimum between them: $D(\alpha) \le P^\star \le P(w)$. A small gap certifies a near-optimal answer without knowing the optimum, which is why it is the stopping rule of every serious convex solver.
:::
::::

:::exercise{ref=e10}
:::

:::exercise{ref=e11}
:::

:::exercise{ref=e12}
:::
