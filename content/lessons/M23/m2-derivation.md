# Derivation: multivariate distributions and the Gaussian

## 1. Joint, marginal and conditional

Several random variables on one sample space have a **joint distribution**: a table $P(X = i, Y = j)$ or a density $p(x, y)$. Summing or integrating out one variable gives the **marginal** of the other, $p(x) = \int p(x, y)\,dy$; dividing by a marginal gives the **conditional**, $p(y \mid x) = p(x, y)/p(x)$, a distribution over $y$ for each fixed $x$. The variables are **independent** when the joint factorizes, $p(x, y) = p(x)p(y)$, which is the same as $p(y \mid x) = p(y)$ for every $x$.

::::derivation{id=d1 title="Rain and umbrellas"}
:::step
The joint table: rain with umbrella $0.30$, rain without $0.05$, dry with umbrella $0.15$, dry without $0.50$. The marginal probability of seeing an umbrella is [[0.45]].
:::
:::step
Given an umbrella, the probability of rain is $0.30/0.45 =$ [[2/3]].
:::
::::

## 2. Random vectors and covariance matrices

A **random vector** $x = (x_1, \dots, x_d)$ has a **mean vector** $\mu = \mathbb{E}x$ and a **covariance matrix**

$$
\Sigma = \mathbb{E}\big[(x - \mu)(x - \mu)^\top\big], \qquad \Sigma_{ij} = \operatorname{Cov}(x_i, x_j) .
$$

It is symmetric, with the variances on the diagonal. For any fixed vector $a$, linearity gives

$$
\operatorname{Var}(a^\top x) = a^\top \Sigma a \ge 0 ,
$$

so **every covariance matrix is positive semidefinite**, and it is singular exactly when some combination $a^\top x$ has zero variance: one coordinate is a fixed linear function of the others. Under an affine map $y = Ax + b$, the mean becomes $A\mu + b$ and the covariance $A\Sigma A^\top$.

::::derivation{id=d2 title="Combinations"}
:::step
$\Sigma = \begin{pmatrix} 4 & 2 \\ 2 & 3 \end{pmatrix}$. The variance of $x_1 + x_2$ is $4 + 3 + 2 \cdot 2 =$ [[11]].
:::
:::step
The variance of $x_1 - x_2$ is $4 + 3 - 2 \cdot 2 =$ [[3]].
:::
:::step
The correlation of $x_1$ and $x_2$ is $2/\sqrt{4 \cdot 3} \approx$ [[0.577|tol=0.002]].
:::
::::

## 3. The multivariate Gaussian and its ellipses

From M20, the Gaussian with mean $\mu$ and covariance $\Sigma$ has density

$$
p(x) = \frac{1}{(2\pi)^{d/2}\sqrt{\det\Sigma}} \exp\Big(-\tfrac12 (x - \mu)^\top \Sigma^{-1} (x - \mu)\Big) .
$$

It depends on $x$ only through the **Mahalanobis distance** $r^2 = (x - \mu)^\top \Sigma^{-1} (x - \mu)$. Write $\Sigma = V \Lambda V^\top$ with orthonormal eigenvectors (the spectral theorem); in the coordinates $c = V^\top(x - \mu)$,

$$
r^2 = \frac{c_1^2}{\lambda_1} + \dots + \frac{c_d^2}{\lambda_d} .
$$

The contour $r = k$ is an ellipse (an ellipsoid) with axes along the eigenvectors and half-lengths $k\sqrt{\lambda_i}$: the eigenvectors of the covariance are the directions of independent variation, and the eigenvalues their variances. In two dimensions $r^2$ of a Gaussian sample has the density $\frac12 e^{-r^2/2}$, so the fraction inside the $k$-sigma ellipse is $1 - e^{-k^2/2}$.

:::widget{name=EigenFlow preset=sym}
:::

The matrix $\begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$ above, read as a covariance, has eigenvalues 3 and 1 along $(1, 1)$ and $(1, -1)$: its density ellipses are stretched along the direction that power iteration finds.

::::derivation{id=d3 title="Reading an ellipse"}
:::step
For $\Sigma = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$, the 1-sigma ellipse has half-axis $\sqrt3 \approx$ [[1.732|tol=0.002]] along $(1, 1)$ and 1 along $(1, -1)$.
:::
:::step
The fraction of samples inside the 2-sigma ellipse is $1 - e^{-2} \approx$ [[0.8647|tol=0.0005]].
:::
::::

::::predict{id=p3 kind=choice answer=b}
In one dimension, 68 percent of a Gaussian lies within one standard deviation of the mean. What fraction of a two-dimensional Gaussian lies inside its 1-sigma ellipse?

- 68 percent
- 39 percent
- 50 percent
- 95 percent

:::reveal
39 percent: $1 - e^{-1/2} \approx 0.393$. A point must be close in both directions at once, and in $d$ dimensions the fraction inside the 1-sigma ellipsoid keeps falling: most of a high-dimensional Gaussian lives in a thin shell at radius about $\sqrt d$, M20's vanishing ball seen from the inside.
:::
::::

## 4. Sampling, whitening and principal axes

If $z$ is standard normal in $d$ dimensions and $\Sigma = LL^\top$ (Cholesky), then $x = \mu + Lz$ has covariance $L I L^\top = \Sigma$: **sampling** costs one factorization and one triangular product per sample. Running it backwards, $z = L^{-1}(x - \mu)$ **whitens**: the result has identity covariance. Any $W$ with $W\Sigma W^\top = I$ whitens; the symmetric choice $W = \Sigma^{-1/2} = V\Lambda^{-1/2}V^\top$ (ZCA) rotates to the eigenvectors, rescales, and rotates back, and moves the data least.

The eigenvectors of a sample covariance are the **principal components** of M14: PCA reads the axes of the fitted Gaussian's ellipses, longest first.

:::edge{to=M14 text="PCA diagonalizes the covariance matrix; its components are the ellipse axes."}
:::

## 5. Conditioning a Gaussian

Split $x$ into unobserved coordinates $a$ and observed $b$, with blocks $\Sigma_{aa}, \Sigma_{ab}, \Sigma_{bb}$. Define the residual $e = x_a - B x_b$ with $B = \Sigma_{ab}\Sigma_{bb}^{-1}$. Its covariance with $x_b$ is $\Sigma_{ab} - B\Sigma_{bb} = 0$, and for jointly Gaussian variables uncorrelated means independent, so learning $x_b$ tells you nothing more about $e$. Hence

$$
x_a \mid x_b \sim N\Big(\mu_a + \Sigma_{ab}\Sigma_{bb}^{-1}(x_b - \mu_b),\ \ \Sigma_{aa} - \Sigma_{ab}\Sigma_{bb}^{-1}\Sigma_{ba}\Big) .
$$

The conditional mean moves linearly with the observation, along the **regression** of $x_a$ on $x_b$; the conditional covariance, the **Schur complement** of $\Sigma_{bb}$, does not depend on the observed value at all and is never larger than $\Sigma_{aa}$. In two dimensions: $\mathbb{E}[y \mid x] = \mu_y + \rho\frac{\sigma_y}{\sigma_x}(x - \mu_x)$ and $\operatorname{sd}(y \mid x) = \sigma_y\sqrt{1 - \rho^2}$.

::::derivation{id=d4 title="The puzzle"}
:::step
Standardized height and weight with $\rho = 0.5$. Someone 1 standard deviation above average in height is expected to be [[0.5]] standard deviations above average in weight: regression to the mean.
:::
:::step
The conditional standard deviation is $\sqrt{1 - 0.25} \approx$ [[0.866|tol=0.001]] of the unconditional one.
:::
::::

## 6. Fusing measurements and the Kalman filter

A belief $N(m_1, v_1)$ about a quantity and an independent measurement of it with noise variance $v_2$, reading $m_2$, combine by conditioning, which for two Gaussians is multiplying their densities:

$$
\frac{1}{v} = \frac{1}{v_1} + \frac{1}{v_2}, \qquad m = m_1 + K(m_2 - m_1), \quad K = \frac{v_1}{v_1 + v_2} .
$$

**Precisions add**, and the new mean moves toward the measurement by the **gain** $K$: far if the belief is vague, little if the measurement is noisy. A **Kalman filter** tracks a moving quantity by alternating this update with a **predict** step that moves the belief forward with the dynamics and adds the process noise: $m \leftarrow Fm$, $P \leftarrow FPF^\top + Q$. Every step maps Gaussians to Gaussians, so the whole belief is two numbers per coordinate and a covariance.

::::derivation{id=d5 title="One update"}
:::step
Prior variance 4, measurement variance 1: the gain is $K = 4/5 =$ [[0.8]].
:::
:::step
The posterior variance is $1/(\frac14 + 1) =$ [[0.8]].
:::
:::step
Prior mean 10, measurement 12: the posterior mean is $10 + 0.8 \cdot 2 =$ [[11.6]].
:::
::::

:::edge{to=M37 text="Gaussian noise added step by step is a diffusion; undoing it needs the score of the density."}
:::

## Summary

| Idea | Statement | Use |
| --- | --- | --- |
| Marginal, conditional | $p(x) = \int p(x, y)\,dy$, $p(y \mid x) = p(x, y)/p(x)$ | reduce and update |
| Covariance matrix | $\Sigma = \mathbb{E}(x - \mu)(x - \mu)^\top$, positive semidefinite | all variances at once |
| Affine maps | $Ax + b$ has mean $A\mu + b$, covariance $A\Sigma A^\top$ | propagate uncertainty |
| Gaussian contours | ellipses along eigenvectors, half-axes $k\sqrt{\lambda_i}$ | read the shape |
| Cholesky | $x = \mu + Lz$; $z = L^{-1}(x - \mu)$ | sample, whiten |
| Conditioning | mean $\mu_a + \Sigma_{ab}\Sigma_{bb}^{-1}(x_b - \mu_b)$, Schur complement covariance | prediction from partial data |
| Fusion | precisions add, gain $v_1/(v_1 + v_2)$ | Kalman filter |
