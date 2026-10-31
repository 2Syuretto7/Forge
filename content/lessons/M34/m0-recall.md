# Recall bridge: from three dimensions to thousands

M09 measured angles with the dot product; M31 bounded how far an average strays from its mean; M14 read a matrix through the eigenvalues of $X^\top X$. Pictures drawn in two or three dimensions mislead in four thousand: almost all of a ball's volume is near its surface, almost all directions are perpendicular to each other, and a matrix of pure noise has a wide, precisely predictable spectrum. This lesson derives these facts and uses them to explain three design choices in every transformer. Clear your due cards above first.

:::edge{from=M09 text="the dot product returns as near-orthogonality in high dimension"}
:::

:::edge{from=M31 text="concentration inequalities and the union bound"}
:::

:::edge{from=M14 text="the eigenvalues of X^T X and the SVD"}
:::

## What carries over

The dot product and the cosine of the angle (M09); Chernoff's method, Markov's inequality applied to $e^{tX}$, and the union bound (M31); variances of sums of independent variables (M22); singular values and the eigenvalues of $X^\top X$ (M14); and the randomized range finder (M33).
