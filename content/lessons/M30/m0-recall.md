# Recall bridge: from equality constraints to prices

M28 solved equality-constrained problems with Lagrange multipliers and showed that a multiplier is the sensitivity of the optimal value to the constraint. M27 measured distributions with entropy and KL divergence. This lesson handles inequality constraints, where a multiplier can be zero, turns multipliers into a second optimization problem of their own, the dual, and finds that softmax is the answer to a constrained problem. Clear your due cards above first.

:::edge{from=M28 text="convexity and Lagrange multipliers"}
:::

:::edge{from=M27 text="entropy and KL divergence"}
:::

## What carries over

At a minimum of $f$ subject to $g(x) = 0$, $\nabla f + \lambda\nabla g = 0$, and $\lambda$ is minus the rate at which the optimal value changes with the constraint level (M28). Entropy $H(p) = -\sum p\log p$ and $\mathrm{KL}(p\|q) = \sum p\log(p/q) \ge 0$ (M27).
