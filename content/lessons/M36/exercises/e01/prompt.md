# The log-derivative trick on a coin

A policy flips a coin: action 1 with probability $p = \sigma(\theta)$, action 0 otherwise, and receives reward $r_1$ or $r_0$. The expected reward $J(\theta) = pr_1 + (1 - p)r_0$ has gradient $(r_1 - r_0)\,p(1 - p)$. The **log-derivative trick** writes the same gradient as an expectation over the policy's own samples (Section 1):

$$
\nabla_\theta J = \mathbb{E}_x\big[r_x\,\nabla_\theta\log p_\theta(x)\big], \qquad \nabla_\theta\log p_\theta(x) = x - p .
$$

- `sigmoid(t)`, `log_prob(x, theta)`, and `score(x, theta)`: $\nabla_\theta\log p_\theta(x)$.
- `exact_grad(theta, r1, r0)`.
- `estimate_grad(theta, r1, r0, n, rng)`: the average of $r_x\cdot$`score(x, theta)` over $n$ sampled actions.

The tests run a **gradient check** of the score, and confirm that the estimate converges to the exact gradient.

## Hints

1. $\log p_\theta(1) = \log\sigma(\theta)$ and $\log p_\theta(0) = \log(1 - \sigma(\theta))$; both derivatives combine into $x - p$.
2. Sample actions with `rng.random(n) < p`.
3. The estimator never differentiates the reward: it only needs the reward's value for each sample.
