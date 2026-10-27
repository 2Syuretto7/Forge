# Break it: heavy tails and tiny samples

Two failure modes of estimation, both common in machine learning practice.

## Heavy tails

Loss values, gradient norms and per-token log-likelihoods are often heavy-tailed: most values are modest and a few are enormous. When the tails are heavy enough, the variance is infinite and the theorems of Section 7 stop applying. The Cauchy distribution is the extreme case.

::::predict{id=p6 kind=choice answer=d}
You average 1,000 draws from a standard Cauchy distribution, and repeat that many times. How spread out are the averages compared with single draws?

- About $\sqrt{1000} \approx 32$ times narrower.
- About 2 times narrower.
- About 32 times wider.
- Exactly as spread out as single draws.

:::reveal
The mean of $n$ independent standard Cauchy variables is again standard Cauchy, for every $n$. Averaging buys nothing. The median, by contrast, concentrates like $1/\sqrt{n}$. Robust statistics such as medians, trimmed means and clipping exist for exactly this situation; gradient clipping in L19 is one of them.
:::
::::

:::exercise{ref=e11}
:::

## Tiny samples

The maximum likelihood estimate is the best fit to the data you have. With three observations, that fit can declare an event impossible because it has not happened yet. Any model that later assigns probability zero to something that does happen has infinite log-loss: a single surprise wipes out every other prediction.

:::exercise{ref=e12}
:::

## What to take away

- Before trusting an average, ask whether the data could have heavy tails. Look at the largest values, not only the mean.
- Never let an estimated probability be exactly 0 or 1 when it will be scored by log-loss. Smoothing (a prior) is the principled fix, and language models get the same protection from the softmax, which never outputs an exact zero.
- The prior's influence fades as data accumulate: with 500 flips the smoothed and unsmoothed estimates are indistinguishable.

:::aside[Why a softmax never outputs exactly zero, and why that is not enough]
$e^{z} > 0$ for every finite $z$, so a softmax assigns positive probability to every class. But it can assign $10^{-30}$, which in float32 rounds to zero, and $-\log(10^{-30}) = 69$ nats of loss on one token. L04 shows how to compute log-softmax without ever forming the tiny probability.
:::
