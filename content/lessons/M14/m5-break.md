# Break it: no centring, squared condition numbers, float32

## Forget to centre

::::predict{id=p5 kind=choice answer=a}
You run PCA on embeddings whose mean vector is long compared with their spread, but forget to subtract the mean. What does the first component find?

- Essentially the direction of the mean: it explains the offset of the cloud from the origin, not its shape.
- The same first component as with centring.
- The direction of least variance.
- Nothing: the SVD fails without centring.

:::reveal
The direction of the mean. Without centring, the SVD fits subspaces through the origin, and the best one-dimensional fit to a cloud far from the origin points at the cloud. The "explained variance" of that component is mostly the squared length of the mean, and every later component is distorted as it must stay perpendicular to it.
:::
::::

:::exercise{ref=e13}
:::

## Square the condition number

:::exercise{ref=e14}
:::

## Single precision on an ill-conditioned matrix

:::exercise{ref=e15}
:::

:::widget{name=MatrixTransform a=1 b=1 c=1 d=1.0001}
:::

Singular values about 2 and $0.00005$: a condition number of 40,000. The ellipse is a needle. Solving with this matrix loses about 4.6 digits in double precision, and in single precision, with about 7 digits to start with, nearly all of them.

## What to take away

- Centre before PCA, unless the offset is what you want to measure.
- Compute singular values from $A$, not from $A^\top A$.
- Before trusting a solution, compare $\log_{10}\kappa$ with the digits your precision carries.
