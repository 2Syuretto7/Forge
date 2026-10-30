# Break it: a kink, a jump, and h = 1e-15

## Differentiating at a corner

:::exercise{ref=e13}
:::

## Differentiating across a jump

:::exercise{ref=e14}
:::

## A step too small to see

::::predict{id=p5 kind=choice answer=d}
You compute the forward difference of $f(x) = x^2$ at $x = 10^8$ with $h = 10^{-9}$. What comes out?

- About $2 \times 10^8$, the right answer.
- About $2 \times 10^8$ with a few wrong digits.
- An overflow error.
- Exactly 0.

:::reveal
Exactly 0. Near $10^8$ doubles are spaced about $1.5 \times 10^{-8}$ apart, so $10^8 + 10^{-9}$ rounds to $10^8$: $f(x + h) - f(x) = 0$ exactly. A step must be scaled to the size of $x$, as in $h = \sqrt{\varepsilon}\max(1, |x|)$; the gradient checkers of M18 do this.
:::
::::

:::exercise{ref=e15}
:::

:::widget{name=TangentZoom f=relu a=0 zoom=12}
:::

At twelve halvings the ReLU's corner is exactly as sharp as at zero halvings. A central difference straddling it reports $1/2$, the average of the two sides, which looks like a derivative and is not one.

## What to take away

- A finite difference near a corner or a jump measures the corner, not a derivative.
- Scale the step to the input, and never go below about $10^{-8}$ relative for forward differences.
- Check a derivative at several points away from corners, with a relative error.
