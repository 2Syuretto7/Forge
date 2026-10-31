# Break it: one test set, many looks

::::predict{id=p5 kind=choice answer=c}
A thousand models that only guess are evaluated on one test set of 1,000 examples, and the best is reported. What accuracy does it report?

- About 50 percent.
- About 52 percent.
- About 55 percent.
- About 70 percent.

:::reveal
About 55 percent: the maximum of 1,000 noisy estimates with standard error $1.6$ points sits about $3.2$ standard errors above the truth. A single-model Hoeffding interval, $\pm 4.3$ points, excludes the true 50 percent; the union bound's $\pm 7.3$ does not. Combining models adaptively can push the reported score far higher still.
:::
::::

:::exercise{ref=e13}
:::

:::exercise{ref=e14}
:::

## Examples that are not independent

:::exercise{ref=e15}
:::

## What to take away

- Count every model you compared before reading a test score.
- Keep a test set that has never influenced a decision, and use it once.
- Check independence: duplicates and leakage shrink the effective sample size silently.
