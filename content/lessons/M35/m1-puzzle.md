# Puzzle: five runs and a forecast

Five small training runs, spread evenly over a factor of 100 in compute, give losses that sit on a straight line on log-log axes. The fit is beautiful. You now want the loss of a run with $100$ times the compute of the largest.

::::predict{id=p1 kind=choice answer=c}
The five points scatter around the fitted line with residual standard deviation $s$ (in log loss). How wide is an honest 95 percent prediction interval for the new run, a hundred times beyond the data?

- About $\pm 2s$, as inside the data.
- About $\pm 3s$.
- About $\pm 7s$.
- About $\pm 50s$.

:::reveal
About $\pm 7s$. Two factors multiply: the distance from the data inflates the standard error by $\sqrt{1 + \frac15 + \frac{(u_0 - \bar u)^2}{\sum(u_i - \bar u)^2}} \approx 2.2$, and with only 5 points and 2 fitted parameters the noise level is so poorly known that Student's $t$ quantile, $3.18$, replaces $1.96$. A beautiful fit to five points is a weak forecast.
:::
::::

::::predict{id=p2 kind=choice answer=b}
Suppose you use the naive band, $\pm 1.96$ standard errors, still with five runs. How often does it contain the new run's loss?

- About 95 percent of the time.
- About 86 percent of the time.
- About 50 percent of the time.
- About 20 percent of the time.

:::reveal
About 86 percent, measured over 4,000 simulated forecasts in e15. The band is a third too narrow; Student's quantile restores 95 percent. And this assumes the law's form is right beyond the data, which the last part of this lesson questions.
:::
::::

Fit runs over a compute range and extrapolate to a target. Switch between a pure power law and one with a floor, and move the target further out.

:::widget{name=ScalingFit lo=18 hi=20 target=22 fit=pure}
:::

## Questions to carry into the derivation

1. Why do loss curves follow power laws, and what does a straight line on log-log axes assume?
2. How do you fit a law that is not linear in its parameters?
3. How much should you trust a fitted exponent, and a prediction far beyond the data?
4. What can no error bar protect you from?
