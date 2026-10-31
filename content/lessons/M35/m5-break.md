# Break it: forecasts that fail with confidence

::::predict{id=p5 kind=choice answer=c}
Data from $L = 1.7 + 2x^{-0.5}$ on $x \in [1, 100]$, fitted by a straight line on log-log axes. What does the line predict at $x = 10^5$?

- About the right value, 1.706.
- About 10 percent too high.
- A loss below the floor of 1.7.
- Exactly 1.7.

:::reveal
A loss below the floor, which no model can reach. The straight line keeps falling at its fitted slope for ever. The fit with a floor predicts within a fraction of a percent. e13 measures both.
:::
::::

:::exercise{ref=e13}
:::

Fit only one decade of compute and extrapolate five decades out, first as a pure power law and then with a floor.

:::widget{name=ScalingFit lo=18 hi=19 target=24 fit=pure}
:::

:::exercise{ref=e14}
:::

## Too few runs

:::exercise{ref=e15}
:::

## What to take away

- Fit the floor; a pure power law extrapolates through it.
- Use Student's quantile, or the bootstrap, when the runs are few.
- A narrow band is a statement about noise, not about the law: check the form with a run closer to the target.
