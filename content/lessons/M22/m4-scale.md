# Scale: ten million samples and a sampler test

A sample mean is itself a random variable, with standard deviation $\sigma/\sqrt n$. At $n = 10^7$ that predicts how many digits of the true mean the sample gets right, and a correct sampler must land within a few such units of the truth every time.

::::predict{id=p4 kind=choice answer=b}
You average $10^7$ draws of an Exponential(1) variable, whose mean and standard deviation are both 1. How far from 1 do you expect the average to land?

- About $10^{-7}$.
- A few times $10^{-4}$.
- About $10^{-2}$.
- About $0.1$.

:::reveal
A few times $10^{-4}$: the standard error is $1/\sqrt{10^7} \approx 3.2 \times 10^{-4}$, so the average gets three or four digits right. Ten million samples buy precision only at the rate $\sqrt n$; another digit costs a hundred times more samples.
:::
::::

:::exercise{ref=e10}
:::

:::exercise{ref=e11}
:::

:::exercise{ref=e12}
:::

Draw 2,000 exponential waiting times. The sample variance lands near $1/\lambda^2$; shrink the sample to 20 and watch both moments wander.

:::widget{name=DistributionPlayground dist=exponential lam=1 n=2000}
:::
