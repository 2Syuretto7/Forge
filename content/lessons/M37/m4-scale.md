# Scale: steps, schedules, end times and real data

::::predict{id=p4 kind=choice answer=c}
With the exact score, 20 reverse steps, uniform in time from $T = 4$ down to $0.001$, against 20 steps on a geometric grid that crowds them near 0. How do the two compare?

- About the same.
- The uniform grid is better: its steps near 0 are as long as anywhere.
- The geometric grid is much better.
- Neither works with 20 steps.

:::reveal
The geometric grid is much better, by more than a factor of two in $W_1$ in e10. Near $t = 0$ the score of the narrow data components changes rapidly and needs short steps; near $T$ everything is a smooth Gaussian and long steps are harmless.
:::
::::

:::exercise{ref=e10}
:::

:::exercise{ref=e11}
:::

:::exercise{ref=e12}
:::
