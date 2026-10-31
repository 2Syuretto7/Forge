# Break it: steps, noise levels and memory

::::predict{id=p5 kind=choice answer=b}
Euler-Maruyama on $dx = -2x\,dt + dW$ with step $h = 0.25$. The true stationary variance is $\frac14$. What variance does the simulation settle at?

- $\frac14$, exactly.
- About $\frac13$: a third too large.
- About $\frac18$.
- It explodes.

:::reveal
About $\frac13$: the recursion $v = (1 - 2h)^2v + h$ gives $v = \frac1{2(2 - 2h)} = \frac13$. Past $h = 1$ the factor $1 - 2h$ exceeds 1 in size and the simulation explodes. The exact Ornstein-Uhlenbeck transition has no such limit.
:::
::::

:::exercise{ref=e13}
:::

Shorten $T$ and cut the steps, and watch the samples miss the target.

:::widget{name=DiffusionStepper steps=10 T=1 frac=1}
:::

:::exercise{ref=e14}
:::

:::exercise{ref=e15}
:::

## What to take away

- Keep Euler-Maruyama's step well below the stability limit, or use exact transitions.
- Train the score at every noise level, conditioned on the level.
- Check generated samples against the training set: copies are a failure, not a success.
