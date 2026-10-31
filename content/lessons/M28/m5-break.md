# Break it: too large a step, a bad minimum, a false composition

## Past 2/L

::::predict{id=p5 kind=choice answer=d}
On $\frac12(x^2 + 10y^2)$, where $L = 10$, gradient descent runs with step $0.21$, just above $2/L = 0.2$. What happens?

- It converges, more slowly.
- It converges along $y$ but diverges along $x$.
- It stalls at a point that is not the minimum.
- It converges along $x$ but oscillates with growing amplitude along $y$.

:::reveal
Along $y$ the factor is $1 - 0.21 \times 10 = -1.1$: each step overshoots the floor by 10 percent more than the last, alternating sides, and the iterates blow up. Along $x$ the factor is $0.79$ and that coordinate converges. The steepest direction alone decides stability.
:::
::::

:::exercise{ref=e13}
:::

Set the learning rate just above the limit: one coordinate dies away while the steep one swings wider at every step.

:::widget{name=LossLandscape surface=quadratic kappa=10 loglr=-0.68 beta=0.9}
:::

## Without convexity

:::exercise{ref=e14}
:::

## A composition that is not convex

:::exercise{ref=e15}
:::

## What to take away

- Prove convexity by composition rules or a Hessian; a zero gradient then certifies the answer.
- Keep the step below $2/L$; expect iteration counts proportional to $\kappa$, and rescale to reduce $\kappa$.
- Without convexity, the start decides the answer.
