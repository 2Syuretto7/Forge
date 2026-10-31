# Break it: three data points and dependent data

## Maximum likelihood with three points

:::exercise{ref=e14}
:::

With three draws the fitted Gaussian hugs the sample: its standard deviation, dividing by $n$, is on average well below the truth, and new data look surprising. Draw new samples of three and watch the solid curve jump around the dashed truth.

:::widget{name=DistributionPlayground dist=gaussian mu=0 sigma=1 n=3}
:::

## The bootstrap on dependent data

::::predict{id=p5 kind=choice answer=a}
You bootstrap the mean of 2,000 consecutive daily measurements that follow each other closely, by resampling single days. How does the bootstrap error bar compare with the truth?

- Much too small.
- About right: the bootstrap needs no formula.
- Much too large.
- It cannot be computed.

:::reveal
Much too small. Resampling single days destroys the runs of similar values, so each resample looks like independent data, whose mean varies far less. The true uncertainty is that of a few hundred independent days. Resampling blocks of consecutive days keeps the dependence and fixes it.
:::
::::

:::exercise{ref=e15}
:::

## What to take away

- With few data, the MLE overfits: it can declare possible things impossible.
- A prior is a regularizer, and with little data it is worth having.
- The bootstrap resamples whatever the independent units are: examples, blocks, users, never single correlated points.
