# Scale: timing loops and reading exponents

The derivation predicted that a double loop costs $O(n^2)$ and a triple loop $O(n^3)$. Clocks are noisy, but exponents survive noise when you read them from a log-log fit over a range of sizes.

::::predict{id=p4 kind=numeric answer=3 tol=0.4}
Naive matrix multiplication of two $n \times n$ matrices with three nested Python loops: you time it at $n = 16, 32, 64$ and fit the slope of log time against log $n$. What slope do you expect?

:::reveal
About 3: the inner body runs $n^3$ times, so doubling $n$ multiplies the time by 8. Measured slopes usually land a little below 3 at small sizes, because fixed overheads (setting up lists, calling functions) take a larger share of short runs.
:::
::::

:::exercise{ref=e10}
:::

:::exercise{ref=e11}
:::

## How fast does a geometric series settle?

A geometric series reaches within $\varepsilon$ of its limit after about $\ln \varepsilon / \ln r$ terms. That number grows slowly as $\varepsilon$ shrinks but quickly as $r$ approaches 1: halving the distance from $r$ to 1 doubles the work.

:::exercise{ref=e12}
:::

The widget shows the same story: set the geometric ratio to 0.9, then 0.99, and watch how many terms each needs before the partial sums sit on the limit line.

:::widget{name=SeriesStacker series=geometric r=0.9 logn=2.5}
:::
