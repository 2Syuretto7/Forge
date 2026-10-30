# Derivation: eigenvalues and eigenvectors

## 1. Invariant directions

A nonzero vector $v$ is an **eigenvector** of a square matrix $A$, with **eigenvalue** $\lambda$, when

$$
Av = \lambda v .
$$

$A$ does not turn $v$; it only scales it by $\lambda$ (and flips it if $\lambda < 0$). Any nonzero multiple of $v$ is also an eigenvector, so what matters is the direction.

## 2. The characteristic polynomial

$Av = \lambda v$ says $(A - \lambda I)v = 0$ with $v \neq 0$: $A - \lambda I$ has a nonzero null space, so it is singular, so its determinant is zero (M10, M11):

$$
\det(A - \lambda I) = 0 .
$$

For a $2 \times 2$ matrix this is $\lambda^2 - (\operatorname{tr} A)\lambda + \det A = 0$, a quadratic (M02). In general it is a polynomial of degree $n$, the **characteristic polynomial**, with $n$ roots counted with multiplicity, some possibly complex. The roots add up to the trace and multiply to the determinant.

::::derivation{id=d1 title="Eigenpairs of a symmetric 2 by 2 matrix"}
:::step
For $A = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$, $\operatorname{tr} A = 4$ and $\det A =$ [[3]].
:::
:::step
$\lambda^2 - 4\lambda + 3 = (\lambda - 3)(\lambda - 1)$. The larger eigenvalue is [[3]].
:::
:::step
For $\lambda = 3$, $A - 3I = \begin{pmatrix} -1 & 1 \\ 1 & -1 \end{pmatrix}$, whose null space is spanned by $(1, 1)$. For $\lambda = 1$ the eigenvector is $(1, t)$ with $t =$ [[-1]].
:::
::::

Numerical libraries never compute the characteristic polynomial; its roots are hopelessly sensitive to rounding for large $n$. They use iterations like the one in Section 5, refined.

## 3. Diagonalization

If $A$ has $n$ independent eigenvectors $v_1, \dots, v_n$, put them as the columns of $V$ and the eigenvalues on the diagonal of $\Lambda$. Then $AV = V\Lambda$ column by column, and

$$
A = V \Lambda V^{-1} .
$$

In the eigenvector basis, $A$ acts by scaling each coordinate separately. Powers become easy: $A^k = V \Lambda^k V^{-1}$, and $\Lambda^k$ just raises each eigenvalue to the $k$-th power.

Not every matrix can be diagonalized. The shear $\begin{pmatrix} 1 & 1 \\ 0 & 1 \end{pmatrix}$ has the eigenvalue 1 twice but only one eigenvector direction, $(1, 0)$: it is **defective**. Its powers $\begin{pmatrix} 1 & k \\ 0 & 1 \end{pmatrix}$ grow like $k$, which no diagonal matrix with ones on the diagonal can do. A rotation by $90^\circ$ has eigenvalues $\pm i$ and no real eigenvector at all.

## 4. Symmetric matrices: the spectral theorem

Symmetric matrices, $S^\top = S$, never have these problems. The **spectral theorem**: a real symmetric matrix has real eigenvalues and an orthonormal basis of eigenvectors, so

$$
S = Q \Lambda Q^\top, \qquad Q^\top Q = I .
$$

The orthogonality has a short proof.

::::derivation{id=d2 title="Eigenvectors of a symmetric matrix are perpendicular"}
:::step
Let $Sv_1 = \lambda_1 v_1$ and $Sv_2 = \lambda_2 v_2$ with $\lambda_1 \neq \lambda_2$, and write $c = v_1 \cdot v_2$. Using $Sv_2 = \lambda_2 v_2$, $v_1 \cdot Sv_2 = \lambda_2 c$. Moving $S$ across the dot product (M10: $x \cdot Sy = S^\top x \cdot y$, and $S^\top = S$), the same number is $Sv_1 \cdot v_2 =$ [[l1*c]], writing $l_1$ for $\lambda_1$.
:::
:::step
Subtracting, $(\lambda_1 - \lambda_2)\,c = 0$, and since $\lambda_1 \neq \lambda_2$, $c =$ [[0]].
:::
::::

The widget's ellipse is the image of the unit circle. For a symmetric matrix its axes point along the eigenvectors and have lengths $|\lambda_1|$ and $|\lambda_2|$; the dashed and solid axes coincide. Make $b \neq c$ and they separate.

:::widget{name=MatrixTransform a=2 b=1 c=1 d=2}
:::

::::predict{id=p3 kind=choice answer=a}
Can a real symmetric matrix have complex eigenvalues?

- No, never: its eigenvalues are always real.
- Yes, when its entries are negative.
- Yes, when its determinant is negative.
- Only for matrices larger than 2 by 2.

:::reveal
Never. For $2 \times 2$ the discriminant is $(\operatorname{tr})^2 - 4\det = (a - d)^2 + 4b^2 \geq 0$. In general, if $Sv = \lambda v$ with $v$ complex, then $\bar v^\top S v$ equals its own complex conjugate (because $S$ is real and symmetric) and also equals $\lambda \|v\|^2$, so $\lambda$ is real. Covariance matrices and Hessians are symmetric, which is why their eigenvalues always make sense as variances and curvatures.
:::
::::

## 5. Power iteration

Write a starting vector in the eigenvector basis, $x = c_1 v_1 + \dots + c_n v_n$, with $|\lambda_1| > |\lambda_2| \geq \dots$. Then

$$
A^k x = c_1 \lambda_1^k v_1 + c_2 \lambda_2^k v_2 + \dots = \lambda_1^k \Big( c_1 v_1 + c_2 \big(\tfrac{\lambda_2}{\lambda_1}\big)^k v_2 + \dots \Big) .
$$

All terms but the first shrink relative to it, the slowest by $|\lambda_2 / \lambda_1|$ per step. **Power iteration** multiplies and rescales repeatedly; the direction converges to $v_1$ with error about $|\lambda_2/\lambda_1|^k$, and the **Rayleigh quotient** $\rho(x) = \frac{x^\top A x}{x^\top x}$ then estimates $\lambda_1$. For a symmetric matrix, $\rho(x)$ is a weighted average of the eigenvalues, $\sum_i \lambda_i c_i^2 / \sum_i c_i^2$, so it always lies between the smallest and the largest.

To find other eigenvalues, **shift and invert**: $(A - \mu I)^{-1}$ has the same eigenvectors with eigenvalues $1/(\lambda_i - \mu)$, largest for the $\lambda_i$ nearest to $\mu$. Power iteration on it, **inverse iteration**, finds the eigenvalue nearest any guess $\mu$, very fast when the guess is good.

::::derivation{id=d3 title="How many steps?"}
:::step
With eigenvalues 3 and 1, the error ratio is $1/3$ per step. To shrink it by $10^{-6}$ needs $k$ with $3^{-k} \leq 10^{-6}$, that is $k \geq 6 / \log_{10} 3 \approx$ [[12.6|tol=0.1]], so 13 steps.
:::
:::step
With eigenvalues 1 and $0.99$, the same accuracy needs $k \geq \ln(10^{-6}) / \ln(0.99) \approx$ [[1375|tol=5]] steps: a small gap means slow convergence.
:::
::::

## 6. Quadratic forms and positive definiteness

A symmetric $S$ defines the **quadratic form** $q(x) = x^\top S x$. In the eigenvector basis, with $x = \sum c_i q_i$,

$$
x^\top S x = \lambda_1 c_1^2 + \dots + \lambda_n c_n^2 .
$$

$S$ is **positive definite** when $q(x) > 0$ for every $x \neq 0$, which by this formula means every eigenvalue is positive. The level sets $q(x) = 1$ are then ellipses (ellipsoids) with axes along the eigenvectors, of half-lengths $1/\sqrt{\lambda_i}$. A positive definite matrix has a **Cholesky factorization** $S = LL^\top$ with $L$ lower triangular; trying to compute it is the cheapest test of positive definiteness, since it fails exactly when some $\lambda_i \leq 0$. Covariance matrices (M23) and the Hessians of convex losses (M18, M28) are positive semidefinite.

::::derivation{id=d4 title="Reading a quadratic form"}
:::step
For $S = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$ and $x = (1, -1)$, $x^\top S x = 2 - 1 - 1 + 2 =$ [[2]].
:::
:::step
$x$ is the eigenvector for $\lambda = 1$ and $\|x\|^2 = 2$, which agrees: $1 \cdot 2$. For $S' = \begin{pmatrix} 1 & 2 \\ 2 & 1 \end{pmatrix}$, the same $x$ gives $1 - 4 + 1 = -2$, so $S'$ is not positive definite: its eigenvalues are 3 and [[-1]].
:::
::::

## 7. Markov chains: the eigenvalue 1

A **Markov chain** on $n$ states moves from state $j$ to state $i$ with probability $P_{ij}$; each column of $P$ sums to 1. A probability vector $p$ evolves as $p \mapsto Pp$. A **stationary distribution** satisfies $P\pi = \pi$: it is an eigenvector with eigenvalue 1, scaled to sum to 1. Every column-stochastic matrix has 1 as an eigenvalue (the rows of $P^\top$ sum to 1, so $P^\top \mathbf{1} = \mathbf{1}$, and $P$ and $P^\top$ share eigenvalues), and no eigenvalue exceeds 1 in absolute value. Running the chain is power iteration, so $p$ approaches $\pi$ at the rate $|\lambda_2|$.

::::derivation{id=d5 title="A two-state chain"}
:::step
$P = \begin{pmatrix} 0.9 & 0.5 \\ 0.1 & 0.5 \end{pmatrix}$. Stationarity $P\pi = \pi$ gives $0.1\pi_1 = 0.5\pi_2$, so $\pi_1 = 5\pi_2$ and, summing to 1, $\pi_1 =$ [[5/6]].
:::
:::step
The trace is $1.4$ and one eigenvalue is 1, so the other is [[0.4]]: the distance to $\pi$ shrinks by 0.4 per step.
:::
::::

**PageRank** is the stationary distribution of a random surfer who follows a random link with probability $d$ (usually 0.85) and jumps to a uniformly random page otherwise. The jump makes the chain irreducible, so $\pi$ is unique, and it guarantees $|\lambda_2| \leq d$: about 113 steps reach $10^{-8}$.

:::edge{to=M14 text="the SVD is the spectral theorem applied to A^T A, and it works for every matrix, square or not."}
:::

:::edge{to=M18 text="the Hessian is symmetric; its eigenvalues decide minimum, maximum or saddle."}
:::

:::edge{to=M23 text="the covariance matrix is symmetric and positive semidefinite; its eigenvectors are the principal components."}
:::

:::edge{to=M28 text="convexity of a smooth function means a positive semidefinite Hessian everywhere."}
:::

:::edge{to=M32 text="Markov chains in depth: stationary distributions, mixing time and the spectral gap."}
:::

## Summary

| Idea | Statement | Use |
| --- | --- | --- |
| Eigenpair | $Av = \lambda v$, $v \neq 0$ | invariant directions |
| Characteristic polynomial | $\det(A - \lambda I) = 0$; sum = trace, product = det | small cases by hand |
| Diagonalization | $A = V\Lambda V^{-1}$, $A^k = V\Lambda^k V^{-1}$ | powers, dynamics |
| Spectral theorem | $S = Q\Lambda Q^\top$, real $\lambda$, orthonormal $Q$ | covariances, Hessians |
| Power iteration | error $\sim |\lambda_2/\lambda_1|^k$ | top eigenvector, PageRank |
| Positive definite | all $\lambda_i > 0$; Cholesky exists | convexity, covariance |
| Markov chain | $P\pi = \pi$, rate $|\lambda_2|$ | stationary distributions |
