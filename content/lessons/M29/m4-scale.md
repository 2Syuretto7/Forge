# Scale: a million rows, and iteration counts against kappa

::::predict{id=p4 kind=choice answer=a}
Logistic regression on $10^6$ rows. One epoch of minibatch SGD with batches of 1,000 takes 1,000 steps. How does its arithmetic compare with one full-batch gradient step?

- About the same: every row is touched once in either case.
- 1,000 times more.
- 1,000 times less.
- A million times more.

:::reveal
About the same arithmetic, but a thousand times as many updates. Early in training, when every minibatch points roughly the same way, a thousand cheap noisy steps beat one exact step by far; near the optimum the noise floor takes over and the step size has to shrink.
:::
::::

:::exercise{ref=e10}
:::

:::exercise{ref=e11}
:::

:::exercise{ref=e12}
:::
