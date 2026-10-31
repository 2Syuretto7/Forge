# Scale: a one-in-a-million event

The probability that a standard normal exceeds $4.75$ is about one in a million. Estimating it naively means waiting for a million samples per hit, and an error bar of 10 percent needs a hundred hits.

::::predict{id=p4 kind=choice answer=c}
How many naive samples does a 10 percent error bar on a probability of $10^{-6}$ require?

- About $10^4$
- About $10^6$
- About $10^8$
- About $10^{10}$

:::reveal
About $10^8$: the relative standard error of a frequency is $\sqrt{(1 - p)/(np)} \approx 1/\sqrt{np}$, so 10 percent needs $np = 100$ hits. Importance sampling from a Gaussian shifted to the tail needs a few hundred samples for the same error bar.
:::
::::

:::exercise{ref=e10}
:::

:::exercise{ref=e12}
:::

:::exercise{ref=e11}
:::
