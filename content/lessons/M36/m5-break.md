# Break it: noise, bias and a reward that lies

::::predict{id=p5 kind=choice answer=a}
REINFORCE with a "baseline" that equals the reward of the action just sampled, $b(a) = r_a$. What does the gradient estimate become?

- Exactly zero, every time.
- Unbiased, with very low variance.
- Unbiased, with very high variance.
- The true gradient multiplied by 2.

:::reveal
Exactly zero: $(r_a - b(a))(e_a - \pi) = 0$ for every sample. The proof that baselines are free needed $b$ to be independent of the action; break that and the estimator is biased, here all the way to nothing. e14 also shows $b(a) = \frac12r_a$ halving the gradient.
:::
::::

:::exercise{ref=e13}
:::

:::exercise{ref=e14}
:::

## A reward that is only a proxy

Optimize a proxy reward with and without the KL penalty, and watch the true reward rise and then fall as the penalty weakens.

:::widget{name=RewardKLTradeoff}
:::

:::exercise{ref=e15}
:::

## What to take away

- Always use a baseline that depends only on the state, and normalize rewards.
- Prefer a pathwise gradient whenever the sampler and the objective allow one.
- Regularize toward a reference policy when the reward is learned.
