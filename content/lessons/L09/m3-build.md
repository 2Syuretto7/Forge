# Build: the optimizers from scratch

## Gradient descent and its speed limit

:::exercise{ref=e01}
:::

:::exercise{ref=e02}
:::

## Momentum

:::exercise{ref=e03}
:::

:::exercise{ref=e04}
:::

## Adam

:::exercise{ref=e05}
:::

::::predict{id=p3 kind=choice answer=c}
You run Adam on a loss and then on the same loss multiplied by 1000. How do the two trajectories compare (ignoring $\epsilon$)?

- The second moves 1000 times faster.
- The second moves about 32 times faster, the square root of 1000.
- They are identical.
- The second diverges.

:::reveal
Scaling every gradient by $c$ scales $\hat m$ by $c$ and $\sqrt{\hat v}$ by $c$, so their ratio, and therefore every step, is unchanged. Plain SGD would move 1000 times faster and almost certainly diverge.
:::
::::

## Schedules and initialization

:::exercise{ref=e06}
:::

:::exercise{ref=e07}
:::
