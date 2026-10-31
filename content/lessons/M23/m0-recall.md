# Recall bridge: from one variable to many

M22 described one random variable by its distribution, its mean and its variance, and a pair by their covariance. Data come as vectors: the pixels of an image, the coordinates of an embedding, the position and velocity of a target. This lesson collects the means into a vector and the covariances into a matrix, and finds that M13's eigenvectors are exactly the right tool to read that matrix. Clear your due cards above first.

:::edge{from=M22 text="variance, covariance and the sum rule"}
:::

:::edge{from=M13 text="the spectral theorem and positive definite matrices"}
:::

:::edge{from=M20 text="the n-dimensional Gaussian density from a change of variables"}
:::

## What carries over

$\operatorname{Var}(X + Y) = \operatorname{Var}X + \operatorname{Var}Y + 2\operatorname{Cov}(X, Y)$ becomes $\operatorname{Var}(a^\top x) = a^\top \Sigma a$ for every combination $a$ at once. M20's density $\exp(-\frac12 x^\top\Sigma^{-1}x)$ is the multivariate Gaussian, and M13's quadratic forms describe its shape.
