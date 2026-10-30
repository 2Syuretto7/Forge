# Break it: degree 15, lost orthogonality, and an outlier

## Nonsense coefficients

:::exercise{ref=e13}
:::

## Classical Gram-Schmidt forgets it was orthogonal

:::exercise{ref=e14}
:::

## One point pulls the whole line

Squares weight large residuals heavily, so one wild point can drag the fit. How much it can pull depends on its **leverage**, the diagonal entry $P_{ii}$ of the projection matrix: how far its $x$ lies from the rest.

::::predict{id=p5 kind=choice answer=a}
Twenty points have $x$ between 0 and 1, and one more has $x = 10$. Roughly what is that point's leverage $P_{ii}$ in a line fit?

- Close to 1: the line is forced almost through it.
- About $1/21$, like every other point.
- Exactly 0.
- About 2, since a line has two parameters.

:::reveal
Close to 1. With $P_{ii} \approx 1$, the fitted value at that point is nearly its own $y$, whatever the other twenty say: the line pivots to pass through it. Leverages lie between 0 and 1 and add up to the number of columns (here 2), so a few far points can take most of it.
:::
::::

:::exercise{ref=e15}
:::

:::widget{name=ProjectionExplorer outlier=true snap=true}
:::

With the outlier added, the least-squares line tilts toward it. The residuals still satisfy both dot-product conditions: least squares did exactly what it promises, and the promise is the problem.

## What to take away

- Prefer QR to the normal equations; it loses half as many digits.
- Use modified Gram-Schmidt, or reorthogonalize, or Householder.
- Check leverage before trusting a fit dominated by a few far points.
