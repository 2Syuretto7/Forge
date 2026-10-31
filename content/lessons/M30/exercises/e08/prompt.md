# Maximum entropy with a reward: the Gibbs distribution

Among distributions $p$ over actions with rewards $r$, maximize the expected reward plus $\tau$ times the entropy, $\sum_i p_i r_i + \tau H(p)$, over the simplex. Lagrange's condition $r_i - \tau(\log p_i + 1) - \nu = 0$ gives $p_i \propto e^{r_i/\tau}$: the softmax of $r/\tau$, the **Gibbs distribution** at temperature $\tau$ (Section 6). The optimal value is $V(r) = \tau\log\sum_i e^{r_i/\tau}$.

- `gibbs(r, tau)`: stably, with the maximum subtracted.
- `objective(p, r, tau)`: $\sum p_i r_i - \tau\sum p_i\log p_i$, with $0\log 0 = 0$.
- `value(r, tau)`: $V(r)$, stably.

The tests run a **gradient check**: $\nabla_r V = $ `gibbs(r, tau)`. They also confirm that the Gibbs distribution beats random distributions on the objective, and attains $V$.

## Hints

1. `e = np.exp((r - r.max()) / tau)`.
2. $V(r) = \max r + \tau\log\sum_i e^{(r_i - \max r)/\tau}$.
3. As $\tau \to 0$ the Gibbs distribution concentrates on the best action; as $\tau \to \infty$ it becomes uniform.
