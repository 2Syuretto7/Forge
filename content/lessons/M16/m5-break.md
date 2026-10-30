# Break it: a cycling Newton, an overshooting descent, a maximum found by mistake

## Newton from a bad start

::::predict{id=p5 kind=choice answer=b}
Newton's method on $f(x) = x^3 - 2x + 2$ starting at $x_0 = 0$. What happens?

- It converges to the real root near $-1.77$.
- It alternates between 0 and 1 for ever.
- It diverges to infinity.
- It stops because $f'(0) = 0$.

:::reveal
It cycles: from 0 the tangent ($f = 2$, $f' = -2$) crosses zero at 1, and from 1 ($f = 1$, $f' = 1$) it crosses back at 0. Newton's quadratic convergence is a local promise. Far from a root the tangent can point anywhere; safeguards (a bracket, a damped step, a line search) keep the method honest.
:::
::::

:::exercise{ref=e13}
:::

:::widget{name=TangentZoom f=cbrt a=0 zoom=4}
:::

The cube root has a vertical tangent at its root. Newton's step there is $x - x^{1/3} / (\frac13 x^{-2/3}) = -2x$: every step doubles the distance and flips the side.

## Gradient descent with too large a step

:::exercise{ref=e14}
:::

## Newton finds a maximum

:::exercise{ref=e15}
:::

## What to take away

- Newton is fast near a simple root and unreliable far from one; bracket or damp it.
- Gradient descent needs $\eta < 2/L$; estimate $L$ before choosing $\eta$.
- Newton for minimization only seeks critical points; check $f'' > 0$ or fall back to a descent step.
