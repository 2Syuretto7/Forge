# Scale and measure: conditioning, PCA and compression

The build movement gave you correct tools. This movement measures what they do on realistic inputs: how much errors grow, how much variance a few directions hold, and how much an image compresses before it degrades.

## How bad can conditioning get?

Condition numbers are not exotic. A random $5 \times 5$ Gaussian matrix typically has $\kappa$ in the tens; the Hilbert matrix of size 10 has $\kappa \approx 1.6 \times 10^{13}$; the covariance matrix of features that are nearly duplicates of each other easily reaches $10^{8}$. The first exercise shows that the bound $\kappa$ is not pessimism: specific inputs attain it.

:::exercise{ref=e10}
:::

::::predict{id=p5 kind=numeric answer=5 tol=1}
A matrix has singular values $100$ and $10^{-3}$, so $\kappa = 10^5$. You solve $Ax = b$ in float64, which carries about 16 significant digits. In the worst case, about how many significant digits of $x$ can you lose?

:::reveal
Errors grow by up to $\kappa = 10^5$, so you can lose about 5 digits and keep about 11. The rule of thumb: you lose about $\log_{10} \kappa$ digits to conditioning, whatever the precision.
:::
::::

## PCA on data with structure

PCA is the SVD of centered data. The exercise data has two strong latent factors in six dimensions; the explained variance ratios should make that obvious.

:::exercise{ref=e11}
:::

## Compressing an image

A smooth image is a matrix with fast-decaying singular values. Truncating the SVD keeps the big ones; Eckart-Young says nothing of the same rank does better, and the exercise checks that claim against random competitors.

:::exercise{ref=e12}
:::

Finally, reach the Eckart-Young optimum by gradient descent on a factorization $UV^\top$. Matrix factorization is non-convex, yet gradient descent from a small random start finds the global optimum here. That is not luck: this loss has no spurious local minima, a fact that also underlies why low-rank adapters train reliably.

:::exercise{ref=e13}
:::

:::edge{to=L09 text="L09 shows that gradient descent on a quadratic converges at a rate set by the condition number."}
:::
