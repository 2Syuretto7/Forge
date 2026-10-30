# Scale: sweeping the step from 0.1 to 1e-16

Compute the forward and central differences of $e^x$ at 1 for steps from $10^{-1}$ down to $10^{-16}$ and plot the error. It falls, reaches a minimum, and climbs back up: a V on a log-log plot, with slopes 1 and $-1$ for the forward difference.

::::predict{id=p4 kind=choice answer=b}
Which step gives the most accurate forward difference of $e^x$ at $x = 1$ in double precision?

- $h = 10^{-15}$: the smallest step is closest to the limit.
- About $10^{-8}$: the square root of the machine epsilon.
- About $10^{-3}$.
- Every $h$ below $10^{-4}$ is equally good.

:::reveal
About $10^{-8}$, where truncation ($\frac{h}{2}e$) and rounding ($\varepsilon e / h$) are equal. At $10^{-15}$ the rounding term is about $0.6$: the estimate is wrong in the first digit. The spacing of floating-point numbers near 1, shown in the widget, is what $h$ is fighting.
:::
::::

:::widget{name=FloatFormats value=1}
:::

:::exercise{ref=e10}
:::

:::exercise{ref=e11}
:::

:::exercise{ref=e12}
:::
