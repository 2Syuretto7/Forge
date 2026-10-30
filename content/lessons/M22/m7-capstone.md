# Capstone: a distribution library and the initialization scale

Write eight samplers from uniform random numbers: Bernoulli, binomial, geometric and Poisson by tables of cumulative probabilities, and uniform, exponential, Laplace and Gaussian by inverse CDFs and Box-Muller. Each must pass a CDF-distance test at a million samples. Then derive the weight scale that preserves the variance of activations through layers with a leaky ReLU, and verify it through 40 layers.

:::exercise{ref=capstone}
:::

## When you finish

You can describe uncertainty with numbers, compute its averages and spreads, and generate it on demand. M23 takes several variables at once and their covariance matrix; M24 studies the average of many samples, whose spread you now know shrinks like $1/\sqrt n$; M27 measures uncertainty itself in bits.

:::edge{to=M32 text="Markov chains, whose states are random variables drawn one after another."}
:::

:::edge{to=M24 text="limit theorems and Monte Carlo."}
:::
