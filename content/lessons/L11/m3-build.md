# Build: counting, fitting and allocating

## Counting

:::exercise{ref=e01}
:::

:::exercise{ref=e02}
:::

## Fitting

:::exercise{ref=e03}
:::

:::exercise{ref=e04}
:::

:::exercise{ref=e05}
:::

## Allocating

:::exercise{ref=e06}
:::

::::predict{id=p4 kind=choice answer=a}
An IsoFLOP profile trains models of several sizes with the same compute. As the model grows along the profile, the loss:

- First falls, then rises: small models lack capacity, large ones see too few tokens.
- Always falls: larger models are always better.
- Always rises: smaller models train on more tokens.
- Stays the same, since the compute is the same.

:::reveal
At fixed $C$, a larger $N$ means a smaller $D = C/6N$. The parameter term $A N^{-\alpha}$ falls and the data term $B D^{-\beta}$ rises, so their sum has a minimum: the U shape whose bottom is that budget's optimal size. Exercise 7 finds the bottom with a parabola in $\log N$.
:::
::::

:::exercise{ref=e07}
:::
