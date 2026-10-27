# Scale and measure: the CLT, the bootstrap and the two coins

The derivation made three quantitative claims: averages become Gaussian, bootstrap intervals cover the truth at about their nominal rate, and the two-coin probability is about $0.65$. This movement measures all three with thousands of simulated datasets.

## The CLT, measured

::::predict{id=p5 kind=choice answer=b}
You average $n$ draws from an exponential distribution (strongly right-skewed) and standardize the mean. As $n$ grows from 1 to 30, how does the Kolmogorov-Smirnov distance to the standard normal behave?

- It stays roughly constant: skewness never washes out.
- It falls steadily, roughly like $1/\sqrt{n}$.
- It falls to zero exactly at $n = 30$.
- It grows, because more draws mean more extreme values.

:::reveal
The Berry-Esseen theorem bounds the distance by a constant times $\mathbb{E}|X - \mu|^3 / (\sigma^3 \sqrt{n})$, so for a skewed but well-behaved distribution it falls like $1/\sqrt{n}$. Nothing special happens at 30; that number is folklore.
:::
::::

:::exercise{ref=e08}
:::

## Bootstrap coverage

A 95 percent interval procedure should contain the true value in 95 percent of repeated experiments. That is a property of the procedure, not of any single interval. The next exercise runs the procedure 300 times on fresh skewed datasets and counts.

:::exercise{ref=e09}
:::

:::widget{name=DistributionPlayground dist=gaussian mu=0 sigma=1 n=40}
:::

Use the widget to build intuition for what the bootstrap is approximating: each new sample (press "Draw a new sample") gives a different mean and a different fitted curve. The bootstrap tries to reproduce that sample-to-sample variation from a single sample.

## The two coins, settled

:::exercise{ref=e13}
:::

:::edge{to=L23 text="Evaluation harnesses report bootstrap intervals over benchmark items; you will reuse this exact code."}
:::
