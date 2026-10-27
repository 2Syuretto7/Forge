# Break it: the step-size sweep

Time to reproduce the puzzle's V-shaped error curve and to predict its minimum from first principles.

The theory says: the forward difference has truncation error $\tfrac12|f''|h$ and rounding error about $\varepsilon|f|/h$; the central difference has truncation $\tfrac16|f'''|h^2$ and the same rounding error. On a log-log plot, truncation is a line of slope $+1$ (forward) or $+2$ (central), rounding a line of slope $-1$, and the total is a V whose bottom you can compute.

:::exercise{ref=e02}
:::

::::predict{id=p5 kind=choice answer=a}
You run a gradient check in **float32** ($\varepsilon \approx 6 \times 10^{-8}$) with central differences. Which step size is about optimal?

- About $10^{-2}$ to $10^{-3}$.
- About $10^{-5}$, the same as in float64.
- About $10^{-8}$.
- About $10^{-12}$.

:::reveal
The optimum scales like $\varepsilon^{1/3}$: $(6 \times 10^{-8})^{1/3} \approx 4 \times 10^{-3}$. The best achievable error is about $\varepsilon^{2/3} \approx 1.5 \times 10^{-5}$, which is why gradient checks are run in float64. A check in float32 with the float64 step $10^{-6}$ would be dominated by rounding error and fail even for a correct gradient.
:::
::::

## What to take away

- Use central differences, in float64, with $h$ near $10^{-6}$ (for inputs and outputs of order one). Scale $h$ with the size of the input when inputs are large.
- Compare with a **relative** error, and expect agreement around $10^{-8}$ to $10^{-10}$ for a correct gradient. An error near $10^{-3}$ or larger means a bug; something near $10^{-5}$ usually means a kink (ReLU, max, absolute value) close to the test point.
- Never check gradients in float16 or bfloat16. L17 explains how training still works in those formats.

:::aside[The complex-step trick]
For functions built from analytic operations, $f'(x) = \operatorname{Im} f(x + ih)/h + O(h^2)$ with no subtraction at all, so there is no cancellation and $h = 10^{-20}$ works perfectly. It fails for code with absolute values, comparisons or non-analytic functions, which is why dual numbers are the more general tool.
:::
