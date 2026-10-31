# Puzzle: seven heads in ten

A coin lands heads 7 times in 10 flips. What is your best estimate of its probability of heads, and how sure should you be?

::::predict{id=p1 kind=numeric answer=0.145 tol=0.03}
Take $0.7$ as the estimate. What is its standard error, the typical distance between such an estimate and the true probability?

:::reveal
About $0.145$: $\sqrt{0.7 \times 0.3/10}$. Ten flips leave the coin's bias anywhere from roughly $0.4$ to $1$. Section 3 derives this from the curvature of the log-likelihood.
:::
::::

::::predict{id=p2 kind=choice answer=c}
A Bayesian starts from a uniform prior over the coin's probability and updates on the 10 flips. What is the mean of the posterior?

- $0.7$, the same as the frequency.
- $0.5$: the prior keeps it at a fair coin.
- $2/3$: as if one extra head and one extra tail had been seen.
- $0.8$.

:::reveal
$2/3$. The posterior is Beta(8, 4), with mean $8/12$. A uniform prior acts like one imaginary head and one imaginary tail; with ten real flips it moves the estimate a little toward $\frac12$, with a thousand it would hardly matter. The two schools agree with much data and disagree with little, and Movement 7 asks when that matters.
:::
::::

Draw a few flips of a coin with probability $0.7$ and watch the likelihood curve. With 10 flips it is broad; with 500 it narrows around the truth.

:::widget{name=DistributionPlayground dist=bernoulli p=0.7 n=10}
:::

## Questions to carry into the derivation

1. How do you judge an estimator before you know the truth?
2. Which parameter value explains the data best, and how sharply do the data pick it?
3. How does a prior change the answer, and when does it stop mattering?
4. How do you get an error bar when there is no formula?
