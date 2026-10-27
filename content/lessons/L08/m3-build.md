# Build: a tensor autograd engine

You will build the engine in stages. Each exercise's starter contains a working version of the previous stages, so you can always move on, but write each stage yourself before reading ahead.

## Graph basics

:::exercise{ref=e01}
:::

:::exercise{ref=e02}
:::

## A scalar engine first

:::exercise{ref=e03}
:::

## Tensors

:::exercise{ref=e04}
:::

:::exercise{ref=e05}
:::

:::exercise{ref=e06}
:::

::::predict{id=p3 kind=choice answer=a}
You compute `loss = (x * x).sum()` with your engine and call `loss.backward()` twice without resetting gradients. What is `x.grad` compared with the true gradient $2x$?

- $4x$: the second backward adds to the existing gradient.
- $2x$: the second call overwrites.
- An error: a graph can only be traversed once.
- Zero: the second call cancels the first.

:::reveal
Gradients accumulate. Your engine (like PyTorch, if you pass `retain_graph=True` so it is allowed) adds the second pass's contribution to the first. This is deliberate, because accumulation is how a tensor used in several places gets the sum of its contributions; it is also why every training step starts with `zero_grad()`.
:::
::::

:::exercise{ref=e07}
:::

## Modules and training

:::exercise{ref=e08}
:::

:::exercise{ref=e09}
:::
