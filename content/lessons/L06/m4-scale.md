# Scale and measure: the threshold, in numbers

Two experiments test Section 5's claims directly: the smallest singular value of a random design collapses at $p = n$, and the variance of the fitted weights follows the two exact formulas on either side. Then a learning curve shows how error falls with more data.

:::exercise{ref=e08}
:::

::::predict{id=p3 kind=numeric answer=18 tol=3}
Noise only ($y = \epsilon$, $\sigma^2 = 1$), $n = 20$ standard Gaussian points, $p = 18$ standard Gaussian features, least squares. What is the expected squared norm of the fitted weights?

:::reveal
$\sigma^2 p/(n - p - 1) = 18/(20 - 18 - 1) = 18$. Two more features and the formula's denominator would hit zero. The exercise below checks the formula by simulation on both sides of the threshold.
:::
::::

:::exercise{ref=e09}
:::

:::exercise{ref=e13}
:::

:::widget{name=DistributionPlayground dist=gaussian mu=0 sigma=1 n=5}
:::

Draw several samples of size 5 in the widget and watch the fitted curve move: that movement, from one training set to the next, is what the variance term measures. Raise $n$ and the fit stops moving.
