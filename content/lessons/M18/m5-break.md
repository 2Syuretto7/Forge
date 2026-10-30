# Break it: a check that lies, and a saddle in disguise

## A gradient check that passes in float32

:::exercise{ref=e13}
:::

## A saddle that looks like a minimum along the axes

::::predict{id=p5 kind=choice answer=d}
You check $f(x, y) = x^2 + y^2 - 3xy$ at the origin by moving along the $x$ axis and along the $y$ axis. Both times $f$ rises. Is the origin a minimum?

- Yes: it rises in both coordinate directions.
- Yes, because the gradient is zero there.
- It cannot be decided.
- No: along the diagonal $f(t, t) = -t^2$ falls. Only the Hessian's eigenvalues, $5$ and $-1$, settle it.

:::reveal
No. Checking along the axes checks only the diagonal entries of the Hessian (both 2). The off-diagonal $-3$ creates a direction of negative curvature that the axes miss. In high dimensions saddles vastly outnumber minima among critical points, and they look like minima along almost every coordinate.
:::
::::

:::widget{name=GradientField f=hidden x=0.5 y=0.5 phi=45}
:::

Set the point to the origin: the gradient vanishes, and the caption reports eigenvalues 5 and $-1$, a saddle. Away from it, the contours are hyperbolas, not the ellipses of a bowl.

:::exercise{ref=e14}
:::

## Gradient checks at a kink

:::exercise{ref=e15}
:::

## What to take away

- Check gradients in float64 with a tight relative tolerance; float32 hides bugs of a part in a thousand.
- Classify a critical point by the Hessian's eigenvalues, never by the coordinate directions alone.
- Keep check points away from kinks, or the check measures the kink.
