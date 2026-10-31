# The policy gradient theorem

For a tabular softmax policy $\pi(a \mid s) = \mathrm{softmax}(\theta_s)_a$ and the objective $J(\theta) = \sum_s\rho_0(s)V^\pi(s)$, the **policy gradient theorem** says (Section 6)

$$
\nabla_\theta J = \sum_sd^\pi(s)\sum_a\pi(a \mid s)\,\nabla_\theta\log\pi(a \mid s)\,Q^\pi(s, a), \qquad d^\pi = \rho_0^\top(I - \gamma P_\pi)^{-1} ,
$$

where $d^\pi$ counts discounted visits. Nothing differentiates the dynamics: they enter only through $Q^\pi$ and $d^\pi$, which samples estimate. For the softmax, the component for $\theta_{s,a}$ is $d^\pi(s)\,\pi(a \mid s)\,(Q^\pi(s, a) - V^\pi(s))$.

- `policy(theta)`: row-wise softmax.
- `objective(P, R, theta, rho0, gamma)`: $J(\theta)$ by exact policy evaluation.
- `policy_gradient(P, R, theta, rho0, gamma)`: the theorem's gradient, computed exactly.

The tests run a **gradient check**: the theorem's gradient matches finite differences of $J$ on a random MDP.

## Hints

1. $Q^\pi(s, a) = R(s, a) + \gamma\sum_{s'}P(s' \mid s, a)V^\pi(s')$.
2. $d^\pi$ is a row vector: solve $(I - \gamma P_\pi)^\top d = \rho_0$.
3. The difference $Q^\pi - V^\pi$ is the **advantage**; the theorem already contains a baseline.
