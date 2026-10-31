# Scale: 200 model sizes, 10,000 test sets, a thousand dimensions

::::predict{id=p4 kind=choice answer=a}
Random-features regression on 100 training points, with the minimum-norm least-squares fit, for every number of features from 1 to 200. Where is the test error worst?

- At 100 features, exactly the number of training points.
- At 200 features, the most complex model.
- At 1 feature, the simplest.
- Nowhere in particular: it rises steadily.

:::reveal
At 100 features: the interpolation threshold. There the fit must pass through every noisy point with a single solution, whose norm, and variance, explode. With more features the minimum-norm interpolant spreads the fit out and the error falls again. A small ridge penalty removes the peak.
:::
::::

:::exercise{ref=e10}
:::

The same double descent with a smooth curve: raise the regularization and the spike at the threshold disappears.

:::widget{name=BiasVarianceCurve n=20 noise=0.3 loglambda=-9}
:::

:::exercise{ref=e11}
:::

:::exercise{ref=e12}
:::
