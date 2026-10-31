# Break it: variances, cross-entropies and pivots

## The textbook variance

:::exercise{ref=e13}
:::

## Probabilities first, logarithms second

::::predict{id=p5 kind=choice answer=c}
A float32 classifier has logits 0 for the correct class and 120 for another. You compute the softmax, then take minus the log of the correct class's probability. What do you get?

- About 120, the right loss.
- About 104, the largest loss float32 can show.
- Infinity: the probability $e^{-120}$ underflowed to 0 and its logarithm is $-\infty$.
- NaN, because softmax overflowed.

:::reveal
Infinity. Subtracting the maximum keeps the softmax from overflowing, but $e^{-120} \approx 10^{-52}$ is below float32's smallest subnormal, about $1.4 \times 10^{-45}$, so the probability is exactly 0 and the loss infinite; its gradient is NaN. Computing $\operatorname{lse}(z) - z_y$ from the logits gives exactly 120.
:::
::::

:::exercise{ref=e14}
:::

## A tiny pivot

:::exercise{ref=e15}
:::

## What to take away

- Never compute a variance as the mean square minus the squared mean.
- Keep probabilities as logits or log-probabilities until the last moment.
- Pivot, sum in pairs or with compensation, and put accumulators in a wider type.
