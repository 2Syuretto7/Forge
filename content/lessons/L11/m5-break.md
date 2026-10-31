# Break it: narrow fits and untuned learning rates

## Extrapolating a straight line

Set the widget to fit runs between $10^{18}$ and $10^{19}$ FLOPs with a pure power law, then widen the range and switch on the floor.

:::widget{name=ScalingFit lo=18 hi=19 fit=pure}
:::

:::exercise{ref=e11}
:::

## One learning rate for every size

::::predict{id=p5 kind=choice answer=b}
You sweep five model sizes, all at the learning rate that was best for the smallest. Fitting $L - E = k N^{-a}$ to the results gives an exponent that is:

- Correct, since the learning rate only affects training speed.
- Too small: the large models are trained at a rate too high for them and look worse than they are.
- Too large: the large models benefit from the higher rate.
- Undefined.

:::reveal
The best rate falls as models grow. At the small model's rate the large models lose some of their advantage, the fitted curve flattens, and you would conclude that scaling up helps less than it does. Exercise 12 measures the size of the error; retune the rate (or use a parametrization in which it transfers across widths) before fitting.
:::
::::

:::exercise{ref=e12}
:::

## What to take away

- Fit losses in log space, over as wide a range as you can afford, with a floor.
- Hold out your largest run and predict it before looking.
- Bootstrap your fits; the constants are less certain than the predictions.
- Retune the learning rate and schedule length for every size and token count.
