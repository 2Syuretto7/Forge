# Recall bridge: the spectral theorem, for every matrix

M13 diagonalized symmetric matrices with an orthonormal basis, $S = Q\Lambda Q^\top$, and found the top eigenvector by power iteration. Most matrices are not symmetric, many are not even square, and some have no eigenvectors at all. This lesson applies the spectral theorem to $A^\top A$, which is always symmetric, and gets a factorization that works for every matrix. Clear your due cards above first.

:::edge{from=M13 text="the spectral theorem and power iteration"}
:::

:::edge{from=M23 text="the covariance matrix, whose eigenvectors are the principal components, read across the probability strand"}
:::

## What carries over

$A^\top A$ is symmetric and its eigenvalues are never negative, since $v^\top A^\top A v = \|Av\|^2$. Its orthonormal eigenvectors are the input directions that $A$ stretches most and least.
