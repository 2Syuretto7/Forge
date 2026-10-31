# Scale: 10,000 samples, 256 dimensions, a gridworld

::::predict{id=p4 kind=choice answer=d}
At $d = 256$, how many times larger is the per-sample variance of the score-function gradient estimate than that of the reparameterization estimate, for $f(x) = \lVert x\rVert^2$ at $\mu = 0$?

- About the same.
- About 16 times.
- About 256 times.
- About 17,000 times.

:::reveal
About 17,000 times: $(258)(260)/4 \approx 16{,}770$. To match the pathwise estimator's accuracy the score function needs that many more samples. The baseline brings its variance down to $2 \times 256 + 8 = 520$, still 130 times larger. When a pathwise gradient exists, use it.
:::
::::

:::exercise{ref=e10}
:::

:::exercise{ref=e11}
:::

## How much the baseline buys

:::exercise{ref=e12}
:::
