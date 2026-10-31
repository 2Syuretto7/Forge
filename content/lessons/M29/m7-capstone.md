# Capstone: an optimizer zoo

Build gradient descent, heavy ball and Nesterov with their optimal constants, measure their rates on quadratics with condition numbers 10, 100 and 1,000, and hold each within 15 percent of its proved rate. Then show that SGD with an inverse-time step converges like $1/k$, and verify Adam's bias correction by averaging its moving average over many random gradient sequences.

:::exercise{ref=capstone}
:::

## When you finish

You can predict how fast an optimizer converges, why it stalls, and what to change. L05 applies all of it to networks; M32 studies the stationary cloud of constant-step SGD as a Markov chain; M36 meets gradients so noisy that variance reduction becomes the main problem.

:::edge{to=L05 text="the practical optimizers: momentum, Adam, schedules and warm-up."}
:::

:::edge{to=M36 text="score functions, gradient estimators and MDPs."}
:::
