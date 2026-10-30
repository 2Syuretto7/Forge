# Break it: equal pulls, a shear, a rotation

## Two eigenvalues of equal size

::::predict{id=p5 kind=choice answer=b}
Power iteration on $\begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$ (eigenvalues $1$ and $-1$) from $(1, 0)$. What happens?

- It converges to $(1, 1)/\sqrt 2$, the eigenvector of 1.
- It alternates between $(1, 0)$ and $(0, 1)$ forever.
- It converges to $(1, -1)/\sqrt 2$.
- It blows up.

:::reveal
It swaps the two coordinates every step, so it alternates forever. Both eigenvalues have size 1, so neither component outgrows the other: the ratio $|\lambda_2 / \lambda_1| = 1$ means no convergence at all. Shifting fixes it: $A + I$ has eigenvalues 2 and 0, and converges in one step.
:::
::::

:::exercise{ref=e13}
:::

## A matrix with too few eigenvectors

:::exercise{ref=e14}
:::

## No real eigenvector at all

:::exercise{ref=e15}
:::

:::widget{name=EigenFlow preset=shear steps=20}
:::

The shear has one eigenvector. The iterates crawl toward it, with an angle that shrinks like $1/k$ instead of geometrically: twenty steps still leave a few degrees.

## What to take away

- The gap between the top two eigenvalues sets the speed; no gap, no convergence.
- Check diagonalizability before using $V\Lambda V^{-1}$; symmetric matrices are always safe.
- Complex eigenvalues mean rotation; power iteration on a real vector cannot settle.
