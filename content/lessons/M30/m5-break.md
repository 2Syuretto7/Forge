# Break it: wrong multipliers, extreme temperatures, a gap that will not close

## Read the bug from the residuals

:::exercise{ref=e13}
:::

Put the free minimum inside the disc and then outside. Inside, the multiplier is exactly 0; outside, the minimum slides along the circle and the multiplier grows with the distance. A solver that reports a positive multiplier with the minimum inside has broken complementary slackness.

:::widget{name=KKTGeometry constraint=disc cx=0.4 cy=0.3 level=1.2}
:::

## Temperature to zero and to infinity

::::predict{id=p5 kind=choice answer=d}
You compute a Gibbs distribution as `np.exp(r / tau) / np.sum(np.exp(r / tau))` with rewards of order 1 and $\tau = 10^{-3}$. What comes out?

- The best action with probability nearly 1.
- The uniform distribution.
- Zeros everywhere.
- `nan`: $e^{1000}$ overflows, and infinity divided by infinity is not a number.

:::reveal
`nan`. Subtracting the largest reward first makes the largest exponent 0, and the same formula then returns the correct, nearly one-hot distribution. At $\tau \to \infty$ the stable version correctly returns the uniform distribution.
:::
::::

:::exercise{ref=e14}
:::

## Duality without convexity

:::exercise{ref=e15}
:::

## What to take away

- Check the four KKT residuals; each names a different bug.
- Compute every softmax with the maximum subtracted, at any temperature.
- Trust a zero duality gap only for convex problems.
