# Break it: chains that fail quietly

::::predict{id=p5 kind=choice answer=d}
A target with two equal peaks 12 standard deviations apart. Random-walk Metropolis with step 1 starts in the left peak and runs 20,000 steps. What fraction of the samples land in the right peak?

- About 50 percent.
- About 25 percent.
- About 5 percent.
- Essentially none.

:::reveal
Essentially none. Midway between the peaks the density is $2e^{-18} \approx 3 \times 10^{-8}$ times its value at a peak, and a walker with step 1 must climb down that far one accepted step at a time. The chain looks perfectly healthy, with a smooth trace and a good acceptance rate, while reporting a mean of $-6$ for a target whose mean is 0.
:::
::::

:::exercise{ref=e13}
:::

Set the step very small, then very large, and watch the effective sample size collapse at both ends; then pull the peaks apart until no step size crosses between them.

:::widget{name=MarkovChainSim logstep=-1.5 sep=10 n=10000}
:::

:::exercise{ref=e14}
:::

## Diagnostics across chains

:::exercise{ref=e15}
:::

## What to take away

- Check that the chain can reach every region of the target before trusting it.
- Tune the step by the acceptance rate: about 0.234 for a random walk, 0.574 for MALA.
- Run several chains from scattered starts and read $\hat R$, not only one trace.
