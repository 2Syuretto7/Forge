# Break it: a forgotten Jacobian

## Forget the determinant

::::predict{id=p5 kind=choice answer=a}
$X$ is a standard normal and $Y = 2X + 1$. You write $p_Y(y) = p_X\big((y - 1)/2\big)$, forgetting the factor. What goes wrong?

- The "density" integrates to 2: the shape is right but the total probability is not.
- Nothing: shifting and scaling do not need a Jacobian.
- It integrates to $\frac12$.
- It is negative for $y < 1$.

:::reveal
It integrates to 2. Stretching by 2 doubles every length, so the density must halve; without the factor $\frac12$ every probability computed from it is twice too large. Checking that a transformed density integrates to 1 catches this at once.
:::
::::

:::exercise{ref=e13}
:::

## Forget the absolute value

:::exercise{ref=e14}
:::

## Forget a branch

:::exercise{ref=e15}
:::

:::widget{name=JacobianWarp map=boxmuller s=0.05 t=0.3 size=0.05}
:::

Box-Muller near $u_1 = 0$ sends a small square to a far, thin sliver of huge area: the tails of the normal distribution, sparsely filled. The caption's density factor is $1/|\det J|$; near the origin of the output it is largest.

## What to take away

- Every transformed density carries $|\det J|$; check that it integrates to 1.
- Use the absolute value: a decreasing map has a negative derivative but a positive density.
- Sum over every preimage of a map that is not one to one.
