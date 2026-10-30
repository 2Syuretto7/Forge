# Break it: heavy tails, hidden correlations and plugged-in averages

## No variance

::::predict{id=p5 kind=choice answer=a}
The Cauchy distribution is symmetric about 0 but has no mean and no variance. How does the spread of the average of 1,000 Cauchy draws compare with the spread of a single draw?

- The same.
- About $\sqrt{1000} \approx 32$ times smaller.
- About 1,000 times smaller.
- Larger.

:::reveal
The same. The average of $n$ standard Cauchy variables is again standard Cauchy: rare huge values dominate every average, and averaging more of them brings in more such values. The $\sigma/\sqrt n$ rule assumed a finite $\sigma$. The median, which ignores the size of the extremes, still concentrates.
:::
::::

:::exercise{ref=e13}
:::

:::widget{name=CLTMachine dist=cauchy n=50}
:::

## Variances that do not add

:::exercise{ref=e14}
:::

## An average plugged in

:::exercise{ref=e15}
:::

## What to take away

- Check that a variance exists before trusting an average.
- Variances add only for uncorrelated terms; correlated measurements are worth fewer independent ones.
- Push expectations through sums, never through nonlinear functions.
