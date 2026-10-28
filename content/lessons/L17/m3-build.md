# Build: formats, sums and scales in NumPy

## Rounding to a format

:::exercise{ref=e01}
:::

:::exercise{ref=e02}
:::

:::exercise{ref=e03}
:::

## Accumulation

:::exercise{ref=e04}
:::

::::predict{id=p3 kind=numeric answer=32 tol=0.5}
You add 0.01 to an fp16 running sum, starting from 0, ten thousand times. Where does the sum stop?

:::reveal
At 32. Between 16 and 32 the spacing is $2^{-6} \approx 0.0156$, so each 0.01 rounds up to one full step and the sum grows too fast; at 32 the spacing becomes $2^{-5} = 0.03125$, more than twice the addend, and every addition rounds back. The true sum is 100. Exercise 4 measures it and repairs it two ways.
:::
::::

## Loss scaling

:::exercise{ref=e05}
:::

:::exercise{ref=e06}
:::

## Rounding that keeps small updates

:::exercise{ref=e07}
:::

:::exercise{ref=e08}
:::
