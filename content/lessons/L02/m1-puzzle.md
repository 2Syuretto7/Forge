# Puzzle: two coins, few flips

You have two coins. Coin A lands heads 3 times in 4 flips. Coin B lands heads 6 times in 10 flips. Which coin is more likely to favor heads, and how confident should you be?

::::predict{id=p1 kind=choice answer=c}
Which statement best matches what the data support?

- Coin A favors heads more: $3/4 = 75\%$ beats $6/10 = 60\%$, so we can be confident.
- Coin B is more reliable, so it favors heads more.
- Coin A's estimate is higher, but with 4 flips both coins are consistent with a wide range of biases; the data barely distinguish them.
- Neither coin can be judged until we have at least 30 flips.

:::reveal
The point estimates are $0.75$ and $0.6$, but four flips constrain a coin very little. With a uniform prior, the posterior for coin A is spread over most of $[0.3, 1]$ and for coin B over most of $[0.3, 0.85]$. The probability that A's bias exceeds B's comes out near $0.65$: a mild lean, not confidence. There is no magic sample size such as 30; uncertainty shrinks smoothly, like $1/\sqrt{n}$.
:::
::::

The widget below lets you feel this. Choose the Bernoulli distribution, set the true $p$, and draw samples of size 4 again and again. Watch the estimate jump around and watch how flat the likelihood curve is. Then raise $n$.

:::widget{name=DistributionPlayground dist=bernoulli p=0.6 n=4}
:::

::::predict{id=p2 kind=numeric answer=0.125 tol=0.02}
A fair coin is flipped 4 times. What is the probability that the fraction of heads is exactly $0$ or exactly $1$, so that the maximum likelihood estimate is as extreme as it can be? Give a decimal.

:::reveal
All tails has probability $1/16$ and all heads has probability $1/16$, so together $2/16 = 0.125$. About one time in eight, four flips of a perfectly fair coin produce an estimate of $0$ or $1$: a claim of certainty from almost no evidence. Movement 5 shows what that does to a model's predictions.
:::
::::

## What you need to answer the puzzle properly

1. A model of the data: each flip is an independent Bernoulli draw with unknown $p$.
2. A way to score parameter values against data: the **likelihood**.
3. A way to combine the data with what you believed before: **Bayes' rule** and a **prior**.
4. A way to quantify uncertainty without a model of the parameter: the **bootstrap**.

By the end of the lesson you will compute $P(p_A > p_B \mid \text{data})$ exactly, and you will see why it is about $0.65$ rather than "obviously A".

::::predict{id=p3 kind=sketch answer="0,0.06,0.36,0.82,0.97,0" xlabel="p from 0 to 1" ylabel="likelihood (scaled)"}
Sketch the likelihood $L(p) = p^3(1-p)$ for coin A at $p = 0, 0.2, 0.4, 0.6, 0.8, 1.0$, scaled so that its maximum is 1. Where is the peak?

:::reveal
$L(p) = p^3(1-p)$ peaks at $p = 3/4$, where it equals $27/256$. Scaled values at $0, 0.2, \dots, 1$ are about $0, 0.06, 0.36, 0.82, 0.97, 0$. The curve is broad: values from $0.4$ to $0.95$ all have at least a third of the peak likelihood. A broad likelihood is what "not much evidence" looks like.
:::
::::
