# Break it: singular, impossible and merely uncorrelated

## Fewer samples than dimensions

:::exercise{ref=e13}
:::

Push the correlation toward $\pm 0.95$: the ellipses flatten toward a line, the small eigenvalue heads to zero, and the inverse covariance in the density blows up across the thin direction. A sample covariance from too few points is that flattened ellipse in many directions at once.

:::widget{name=GaussianEllipse sx=1 sy=1 rho=0.95 x0=1 cond=false}
:::

## A matrix that is not a covariance

:::exercise{ref=e14}
:::

## Uncorrelated but dependent

::::predict{id=p5 kind=choice answer=d}
$x$ is standard normal and $y = sx$, where $s = \pm 1$ is an independent fair sign. Both are standard normal and their correlation is 0. Are they independent?

- Yes: zero correlation means independence.
- Yes: both are Gaussian.
- No, because their correlation is secretly nonzero.
- No: $\lvert y\rvert = \lvert x\rvert$ always, so knowing $x$ leaves only two possible values of $y$.

:::reveal
No. Zero correlation implies independence only for a **jointly** Gaussian pair, and this pair is not one: $x + y$ is exactly 0 half the time, which no Gaussian allows. Each variable alone is Gaussian, but the joint distribution lives on the two diagonal lines.
:::
::::

:::exercise{ref=e15}
:::

## What to take away

- A covariance matrix needs many more samples than dimensions; shrink it when it does not have them.
- Factor with Cholesky, and add jitter or repair eigenvalues when it fails.
- "Uncorrelated implies independent" needs joint Gaussianity, not Gaussian marginals.
