# Break it: NaN from softmax and zero from probabilities

The exponential grows so fast that a few dozen units of input exhaust a floating-point format, and products of probabilities shrink so fast that a few hundred of them reach zero. Both failures are silent and both have the same cure: work with logarithms and shift before exponentiating.

## Softmax of large logits

::::predict{id=p5 kind=choice answer=c}
In float64, the naive softmax of the scores $(1000, 999, 998)$ computes $e^{z_i} / \sum_j e^{z_j}$ directly. What does it return?

- The right answer, about $(0.665, 0.245, 0.090)$.
- $(1, 0, 0)$.
- $(\text{nan}, \text{nan}, \text{nan})$.
- An error message.

:::reveal
$e^{1000}$ overflows to infinity, and infinity divided by infinity is "not a number", nan. NumPy prints at most a warning and returns nan for every entry. Subtracting the maximum first gives $e^0, e^{-1}, e^{-2}$ over their sum: $(0.665, 0.245, 0.090)$, exactly what the softmax should be.
:::
::::

:::exercise{ref=e13}
:::

## A thousand small probabilities

The probability of a 1,000-token text under a model is a product of 1,000 per-token probabilities. At 0.01 each, that is $10^{-2000}$, far below the smallest float64 ($\approx 10^{-308}$). The product underflows to 0 and its log is $-\infty$. Sum the logs instead.

:::exercise{ref=e14}
:::

## The bounds that make the shift safe

:::exercise{ref=e15}
:::

## What to take away

- Never exponentiate raw scores. Subtract the maximum (softmax), or factor it out of the logarithm (log-sum-exp).
- Never multiply many probabilities. Add their logarithms.
- When a computation returns nan or infinity, look for an exponential or a product one step earlier.
