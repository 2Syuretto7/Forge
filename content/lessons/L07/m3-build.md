# Build: an MLP with a hand-written backward pass

Seven exercises, built in the order you would build a library: one module per layer type, each with its own gradient check, then the whole network, then a dataset and a training loop. Four exercises include gradient checks; a mistake in any layer shows up there first.

## Layers

:::exercise{ref=e01}
:::

:::exercise{ref=e02}
:::

:::exercise{ref=e03}
:::

## The network

:::exercise{ref=e04}
:::

::::predict{id=p3 kind=numeric answer=0.000001 tol=0.00002}
Your MLP's backward pass is correct. You check the gradient of $W_1$ with central differences at $h = 10^{-6}$ in float64 and compute the relative error. Roughly what value do you expect, to within an order of magnitude? Enter it as a decimal (the accepted range is generous).

:::reveal
Values around $10^{-8}$ to $10^{-10}$ are typical for a correct gradient of a smooth network; ReLU kinks near the test point can push it toward $10^{-6}$. Anything near $10^{-3}$ or larger means a bug. The tests in this course use $10^{-5}$ as the cutoff.
:::
::::

## Data and training

:::exercise{ref=e05}
:::

:::exercise{ref=e06}
:::

:::exercise{ref=e07}
:::
