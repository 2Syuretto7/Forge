# Scale: 50 dimensions, tuned proposals, 20,000 parallel chains

::::predict{id=p4 kind=choice answer=c}
A 50-dimensional Gaussian target with scales between $0.5$ and $1$. Random-walk Metropolis and MALA each run 8,000 steps, each with a sensible step size. How much larger is MALA's effective sample size, for the worst coordinate?

- About the same.
- About twice.
- Tens of times larger.
- Thousands of times larger.

:::reveal
Tens of times: in the exercise below it comes out near 30. The random walk's step must shrink like $d^{-1/2}$ to keep any proposals accepted, MALA's only like $d^{-1/3}$, because its drift points the proposal where the density is. Gradients buy speed, and the advantage grows with the dimension.
:::
::::

:::exercise{ref=e10}
:::

:::exercise{ref=e11}
:::

## Many chains at once

:::exercise{ref=e12}
:::
