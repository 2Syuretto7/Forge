# Scale: ten thousand small turns

Rotations are exact in mathematics and approximate in floating point. Turn a shape of 1,000 points through a full circle in 10,000 small steps and measure how far it drifts from where it started.

The widget below is the rotation as a matrix: set $a = d = \cos\theta$, $c = \sin\theta$ and $b = -\sin\theta$ for some angle (try $\theta = 30^\circ$: $0.87, -0.5, 0.5, 0.87$). The determinant is 1 and both singular values are 1: a rotation neither stretches nor squashes anything.

:::widget{name=MatrixTransform a=0.87 b=-0.5 c=0.5 d=0.87}
:::

::::predict{id=p4 kind=choice answer=b}
In float64, 10,000 small rotations bring each point back to (almost) where it started. About how far is it off?

- About $10^{-3}$: the errors add up over 10,000 steps.
- Around $10^{-12}$: each step adds a rounding error near $10^{-16}$, and 10,000 of them add up to at most about $10^{-12}$.
- Exactly 0.
- About 1: rounding errors grow exponentially.

:::reveal
Each step rounds each coordinate to about 16 significant digits, so it errs by about $10^{-16}$. Over 10,000 steps those errors accumulate to somewhere between $\sqrt{10^4} \times 10^{-16} = 10^{-14}$ (if they partly cancel, like M01's estimates) and $10^4 \times 10^{-16} = 10^{-12}$ (if they all push the same way). The exercise measures it: about $1.6 \times 10^{-12}$, the worst case, because the rounding errors of a rotation tend to push the same way. In float32 the same experiment drifts by nearly $10^{-3}$.
:::
::::

:::exercise{ref=e10}
:::

:::exercise{ref=e11}
:::

## Rotary encodings at scale

:::exercise{ref=e12}
:::
