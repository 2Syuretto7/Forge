# Capstone: an optimization lab

Predict, then measure. For ten quadratics, with condition numbers from 10 to 1,000 and two choices of step, predict from the eigenvalues how many iterations gradient descent needs to reduce the error a millionfold, run it, and compare. Every run must land within 15 percent of its prediction and below the worst-case rate bound.

:::exercise{ref=capstone}
:::

## When you finish

You can tell an easy optimization problem from a hard one before running anything: convex or not, and how ill-conditioned. M29 attacks the condition number with momentum and adaptive steps, and adds the noise of stochastic gradients; M30 handles inequality constraints with duality.

:::edge{to=M30 text="constrained optimization, Lagrange duality and KKT."}
:::

:::edge{to=M29 text="gradient methods: convergence, momentum and noise."}
:::
