# Break it: light tails, infinite variance and correlated samples

## A proposal that never looks where it matters

::::predict{id=p5 kind=choice answer=b}
You estimate an expectation under a Laplace density, whose tails fall like $e^{-\lvert x\rvert}$, by importance sampling from a standard normal, whose tails fall like $e^{-x^2/2}$. What goes wrong?

- Nothing: importance sampling is unbiased for any proposal.
- The estimator is unbiased, but its variance is infinite: estimates usually fall short, now and then a single huge weight overshoots, and the error bars are wrong.
- The estimator is biased upward.
- The weights are all equal, so nothing is gained.

:::reveal
Unbiased, but with infinite variance. The weights $p/q$ grow like $e^{x^2/2 - \lvert x\rvert}$ in the tails, so their second moment diverges. The sample standard deviation is finite and misleading, the CLT interval does not apply, and the average converges painfully slowly. A proposal must have tails at least as heavy as the target's.
:::
::::

:::exercise{ref=e13}
:::

## No variance, no bell curve

:::exercise{ref=e14}
:::

The skewed distribution here takes the value 10 with probability $0.05$. At 30 draws per average the histogram is still lopsided; the bell curve arrives, but slowly, because skewness fades only like $1/\sqrt n$.

:::widget{name=CLTMachine dist=skewed n=30}
:::

## Samples that remember

:::exercise{ref=e15}
:::

## What to take away

- Check that the variance is finite before trusting $s/\sqrt n$.
- Give importance proposals heavier tails than the target, and watch the effective sample size.
- Correlated samples are worth fewer independent ones: use batch means.
