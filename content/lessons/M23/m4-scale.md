# Scale: a Gaussian in 256 dimensions

A covariance matrix in 256 dimensions has 32,896 free entries. Estimating them takes far more data than intuition suggests, and the errors are not random noise around the truth: they spread the eigenvalues in a predictable way.

::::predict{id=p4 kind=choice answer=c}
Draw 256 samples from a standard Gaussian in 256 dimensions, whose true covariance is the identity, all eigenvalues 1. What is the largest eigenvalue of the sample covariance?

- About 1.
- About 1.1.
- About 4.
- About 256.

:::reveal
About 4. The Marchenko-Pastur law puts the sample eigenvalues between $(1 - \sqrt{d/n})^2$ and $(1 + \sqrt{d/n})^2$: from 0 to 4 at $n = d$. The smallest are near zero, so the fitted Gaussian claims almost no spread in some directions, and held-out points get very low density there. Sixteen times as much data still leaves the edges at $0.56$ and $1.56$.
:::
::::

:::exercise{ref=e10}
:::

:::exercise{ref=e11}
:::

:::exercise{ref=e12}
:::
