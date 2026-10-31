# Scale and measure: estimating information from data

Information quantities are expectations under distributions you never see exactly. This movement measures how estimates behave with finite samples, checks a closed form against Monte Carlo, and quantifies how strongly a small KL pins two distributions together.

## Entropy from samples

::::predict{id=p4 kind=choice answer=a}
You estimate the entropy of an 8-outcome distribution by plugging in the empirical frequencies of 20 samples. On average, compared with the true entropy, the estimate is:

- too low
- too high
- unbiased
- too low or too high with equal probability

:::reveal
Too low. With 20 samples some outcomes are missing and the observed frequencies are lumpier than the truth, and lumpier distributions have lower entropy. (Formally, entropy is concave, so by Jensen's inequality the expected plug-in value is below the entropy of the expected frequencies.)
:::
::::

:::exercise{ref=e08}
:::

## Gaussians: closed form against Monte Carlo

:::exercise{ref=e09}
:::

## How much does a small KL guarantee?

:::exercise{ref=e03}
:::

## Bits per character of a text

:::exercise{ref=e14}
:::

:::widget{name=EntropyBars k=5 p="5,3,1,1,0.5" q="4,3,2,1,1"}
:::

Use the widget to explore the asymmetry: make $q$ put almost no mass on an outcome where $p$ has some, and watch $\mathrm{KL}(p\|q)$ explode while $\mathrm{KL}(q\|p)$ stays modest. Then do the reverse.
