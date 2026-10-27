# Derivation: from projections to the SVD

This movement builds the whole toolkit in one connected line of reasoning: projections lead to least squares, least squares leads to orthogonal bases and QR, symmetric matrices lead to eigenvectors, eigenvectors of $A^\top A$ lead to the SVD, and the SVD explains both puzzles. Take it in sittings; each section ends with a derivation you complete yourself.

## 1. Data as a matrix

A dataset of $n$ points in $\mathbb{R}^d$ is a matrix $X \in \mathbb{R}^{n \times d}$ with one point per row. A matrix also acts on vectors: $A \in \mathbb{R}^{m \times n}$ sends $x \in \mathbb{R}^n$ to $Ax \in \mathbb{R}^m$, and $Ax$ is a weighted sum of the columns of $A$ with weights $x_1, \dots, x_n$. So the set of all outputs $\{Ax\}$ is the **column space** of $A$: every combination of its columns.

A set of vectors is a **basis** for a space if every vector in the space is exactly one combination of them. The number of basis vectors is the **dimension**. The dimension of the column space is the **rank** of $A$. If $A$ is $m \times n$ with $m > n$ and rank $n$, its column space is an $n$-dimensional flat slice through $\mathbb{R}^m$, and most vectors $b \in \mathbb{R}^m$ are not in it. That is the normal situation in data fitting: more equations than unknowns, no exact solution.

## 2. Projection onto a line

Start with the simplest version of "closest point": the point on the line through the origin in direction $a$ that is closest to $b$. Points on the line are $t a$ for scalars $t$. We minimize the squared distance $f(t) = \|b - t a\|^2$.

::::derivation{id=d1 title="The closest point on a line"}
:::step
Write $s = a^\top b$ and $q = a^\top a$. Expanding the square, $f(t) = b^\top b - 2 t s + t^2 q$. Its derivative is $f'(t) =$ [[2*t*q - 2*s]].
:::
:::step
Setting $f'(t) = 0$ gives the best scalar $t^\star =$ [[s/q]], that is $t^\star = \dfrac{a^\top b}{a^\top a}$.
:::
:::step
The residual is $r = b - t^\star a$. Its dot product with $a$ is $a^\top b - t^\star a^\top a = s - t^\star q =$ [[0]]. The error is perpendicular to the line.
:::
::::

The projection is $p = \dfrac{a a^\top}{a^\top a}\, b$. The matrix $P = \dfrac{a a^\top}{a^\top a}$ is symmetric ($P^\top = P$) and **idempotent** ($P^2 = P$): projecting twice changes nothing.

## 3. Projection onto a subspace, and least squares

Now replace the line by the column space of $A \in \mathbb{R}^{m \times n}$ (full column rank). We want the $x$ that makes $Ax$ closest to $b$:

$$
x^\star = \arg\min_x \; L(x), \qquad L(x) = \|Ax - b\|^2 .
$$

This is the **least squares** problem. There are two ways to solve it, and both are worth knowing.

**Geometry.** By the same argument as for a line, the residual $r = b - Ax^\star$ must be perpendicular to every direction you could move in, that is to every column of $A$. Stacking those $n$ conditions gives $A^\top (b - A x^\star) = 0$, the **normal equations**:

$$
A^\top A \, x^\star = A^\top b .
$$

**Calculus.** Expand $L(x) = x^\top A^\top A x - 2 b^\top A x + b^\top b$. The gradient of $x^\top M x$ for symmetric $M$ is $2Mx$, and the gradient of $c^\top x$ is $c$, so

$$
\nabla L(x) = 2 A^\top A x - 2 A^\top b = 2 A^\top (Ax - b).
$$

Setting the gradient to zero gives the same normal equations. Check the scalar case to make the matrix formula feel concrete.

::::derivation{id=d2 title="Least squares in one dimension, then in general"}
:::step
With one unknown and one equation, $L(x) = (a x - b)^2$. The derivative is $L'(x) =$ [[2*a*(a*x - b)]].
:::
:::step
So the minimizer is $x^\star =$ [[b/a]] when $a \neq 0$. In the matrix case, $a$ becomes $A$, "multiply by $a$" becomes "multiply by $A^\top$", and division becomes solving with $A^\top A$.
:::
:::step
With $m$ equations in one unknown, $L(x) = \sum_i (a_i x - b_i)^2$. Writing $S_{ab} = \sum_i a_i b_i$ and $S_{aa} = \sum_i a_i^2$, the minimizer is $x^\star =$ [[S_ab/S_aa]], which is exactly $(A^\top A)^{-1} A^\top b$ for a single column.
:::
::::

The fitted vector $\hat b = A x^\star = A (A^\top A)^{-1} A^\top b$ is the projection of $b$ onto the column space, with projection matrix

$$
P = A (A^\top A)^{-1} A^\top, \qquad P^\top = P, \qquad P^2 = P .
$$

You will verify both identities numerically in the build movement.

:::edge{to=L05 text="Linear regression is this least-squares problem; L05 derives the squared loss from Gaussian noise."}
:::

## 4. Orthonormal bases make everything easy

If the columns of $Q$ are **orthonormal** (unit length, mutually perpendicular), then $Q^\top Q = I$ and the normal equations collapse to $x^\star = Q^\top b$: each coefficient is a single dot product. Projection becomes $P = Q Q^\top$. That is why we want orthonormal bases, and **Gram-Schmidt** manufactures one from any independent set $a_1, \dots, a_n$:

$$
v_k = a_k - \sum_{j<k} (q_j^\top a_k)\, q_j, \qquad q_k = \frac{v_k}{\|v_k\|}.
$$

Each step removes from $a_k$ its components along the directions already built, then normalizes what is left. Recording the coefficients gives the **QR factorization** $A = QR$, with $R$ upper triangular, $R_{jk} = q_j^\top a_k$ for $j < k$, and $R_{kk} = \|v_k\| > 0$.

::::derivation{id=d3 title="Least squares through QR"}
:::step
Substitute $A = QR$ into $A^\top A x = A^\top b$. Since $Q^\top Q = I$, the left side becomes $R^\top R x$ and the right side becomes $R^\top Q^\top b$. Because $R$ is invertible, cancel $R^\top$ to get $R x = Q^\top b$. Which kind of substitution solves a triangular system? [[word:back substitution/backward substitution/back-substitution]]
:::
:::step
Gram-Schmidt in two dimensions: $a_1 = (3, 4)$ gives $q_1 = (0.6, 0.8)$. For $a_2 = (1, 0)$, the coefficient $R_{12} = q_1^\top a_2 =$ [[0.6]].
:::
:::step
Then $v_2 = a_2 - 0.6\, q_1 = (1 - 0.36,\; -0.48) = (0.64, -0.48)$, whose length $R_{22} =$ [[0.8]].
:::
::::

In floating point, the classical formula above loses orthogonality when columns are nearly parallel. The **modified** version subtracts each projection from the running vector immediately, one $q_j$ at a time, which is mathematically identical and numerically much better. You will implement the modified form.

## 5. Symmetric matrices and eigenvectors

An eigenvector $v \neq 0$ of a square matrix $S$ satisfies $S v = \lambda v$: $S$ only stretches it. For **symmetric** $S$ the spectral theorem says there is an orthonormal basis of eigenvectors with real eigenvalues, $S = V \Lambda V^\top$. The orthogonality part has a two-line proof.

::::derivation{id=d4 title="Why eigenvectors of a symmetric matrix are orthogonal"}
:::step
Let $S v_1 = \lambda_1 v_1$ and $S v_2 = \lambda_2 v_2$ with $\lambda_1 \neq \lambda_2$. Compute $v_1^\top S v_2$ two ways. Using $S v_2 = \lambda_2 v_2$ gives $\lambda_2\, v_1^\top v_2$. Using $S^\top = S$, $v_1^\top S v_2 = (S v_1)^\top v_2 =$ [[l1*c]] where $c = v_1^\top v_2$ and $l_1 = \lambda_1$.
:::
:::step
Subtracting, $(\lambda_1 - \lambda_2)\, c = 0$, and since $\lambda_1 \neq \lambda_2$ we get $c =$ [[0]].
:::
::::

The **Rayleigh quotient** $\rho(x) = \dfrac{x^\top S x}{x^\top x}$ connects eigenvectors to optimization. Writing $x = \sum_i c_i v_i$ gives $\rho(x) = \dfrac{\sum_i \lambda_i c_i^2}{\sum_i c_i^2}$, a weighted average of eigenvalues. So $\max_x \rho(x) = \lambda_{\max}$, reached at the top eigenvector, and its gradient

$$
\nabla \rho(x) = \frac{2}{x^\top x}\big(Sx - \rho(x)\, x\big)
$$

vanishes exactly at eigenvectors. Remember this: "the direction that maximizes a quadratic form" will be PCA's definition of the first principal component.

**Power iteration** finds the top eigenvector by repeated multiplication: $x_{k+1} = S x_k / \|S x_k\|$. If $x_0 = \sum_i c_i v_i$ with $c_1 \neq 0$, then $S^k x_0 = \sum_i c_i \lambda_i^k v_i$, and every component except the first shrinks relative to it.

::::derivation{id=d5 title="How fast power iteration converges"}
:::step
After $k$ multiplications, the coefficient on $v_2$ relative to the coefficient on $v_1$ has been multiplied by [[(l2/l1)^k]], where $l_1 = \lambda_1$ and $l_2 = \lambda_2$ are the two largest eigenvalues (in absolute value).
:::
:::step
If $\lambda_2 / \lambda_1 = 0.9$, the number of steps needed to shrink that ratio by a factor $10^{-6}$ is $k = \ln(10^{-6}) / \ln(0.9) \approx$ [[131|tol=1]].
:::
::::

A small gap between $\lambda_1$ and $\lambda_2$ means slow convergence. You will measure exactly this.

## 6. The SVD, built from eigenvectors

Every matrix $A \in \mathbb{R}^{m \times n}$, square or not, has a **singular value decomposition**

$$
A = U \Sigma V^\top ,
$$

with orthonormal columns in $U$ and $V$ and nonnegative **singular values** $\sigma_1 \ge \sigma_2 \ge \dots \ge 0$ on the diagonal of $\Sigma$. Here is a construction from the eigen-decomposition you already have.

1. $A^\top A$ is symmetric, and positive semidefinite because $x^\top A^\top A x = \|Ax\|^2 \ge 0$. So $A^\top A = V \Lambda V^\top$ with $\lambda_i \ge 0$.
2. Define $\sigma_i = \sqrt{\lambda_i}$ and, for $\sigma_i > 0$, $u_i = A v_i / \sigma_i$.
3. Then $A v_i = \sigma_i u_i$ for each $i$, which in matrix form is $A V = U \Sigma$, so $A = U \Sigma V^\top$.

The only thing left to check is that the $u_i$ are orthonormal.

::::derivation{id=d6 title="The left singular vectors are orthonormal"}
:::step
$u_i^\top u_j = \dfrac{v_i^\top A^\top A v_j}{\sigma_i \sigma_j} = \dfrac{\lambda_j\, v_i^\top v_j}{\sigma_i \sigma_j}$. For $i = j$ this equals $\lambda_i / \sigma_i^2 =$ [[1]].
:::
:::step
For $i \neq j$ it equals [[0]], because the eigenvectors $v_i, v_j$ are orthogonal.
:::
:::step
The eigenvalues of $A^\top A$ are the squares of the singular values of $A$. If $A^\top A$ has eigenvalues $9$ and $4$, the singular values of $A$ are $3$ and [[2]].
:::
::::

**Geometry.** $V^\top$ rotates, $\Sigma$ stretches along the axes, $U$ rotates again. The unit circle maps to an ellipse whose semi-axes are $\sigma_i u_i$, reached from the inputs $v_i$. Move the sliders and compare the solid arrows (the semi-axes $\sigma_i u_i$) with the dashed ones (the inputs $v_i$).

:::widget{name=MatrixTransform a=1.4 b=0.6 c=0.2 d=0.9}
:::

The SVD also writes $A$ as a sum of rank-one pieces, ordered by importance:

$$
A = \sum_{i=1}^{r} \sigma_i \, u_i v_i^\top .
$$

Computing the SVD this way (through $A^\top A$) is perfect for understanding and fine for well-conditioned matrices, but it squares the condition number. Library routines work on $A$ directly; you will see why that matters in Movement 5.

## 7. The condition number explains puzzle 1

Solve $Ax = b$ for square invertible $A$, and suppose $b$ carries an error $\delta b$. The solution moves by $\delta x = A^{-1} \delta b$.

::::derivation{id=d7 title="How much errors can grow"}
:::step
The largest stretch of $A^{-1}$ is $1/\sigma_{\min}$, so $\|\delta x\| \le \|\delta b\| / \sigma_{\min}$. The largest stretch of $A$ is $\sigma_{\max}$, so $\|b\| = \|Ax\| \le \sigma_{\max} \|x\|$. Multiplying the two inequalities, $\dfrac{\|\delta x\|}{\|x\|} \le \kappa \dfrac{\|\delta b\|}{\|b\|}$ with $\kappa =$ [[smax/smin]], writing smax and smin for $\sigma_{\max}, \sigma_{\min}$.
:::
:::step
The singular values of $A^\top A$ are the squares of those of $A$. So if $A$ has condition number $k$, the normal-equations matrix $A^\top A$ has condition number [[k^2]].
:::
:::step
Floating-point arithmetic rounds each number with relative error about $\varepsilon$: roughly $6 \times 10^{-8}$ in float32 and $1.1 \times 10^{-16}$ in float64. With $\kappa = 10^{8}$, the worst-case relative error in float32 is about $\kappa \varepsilon \approx$ [[6|tol=0.5]], meaning no correct digits.
:::
::::

The puzzle matrix $\begin{pmatrix} 1 & 1 \\ 1 & 1.0001 \end{pmatrix}$ is symmetric with eigenvalues about $2.00005$ and $0.00005$, so $\kappa \approx 40{,}000$. The change $\delta b = (0, 0.0001)$ has relative size $0.0001 / \|(2, 2.0001)\| \approx 3.5 \times 10^{-5}$, so the bound allows a relative change in $x$ of up to $40{,}000 \times 3.5 \times 10^{-5} \approx 1.4$. The actual change, from $(1,1)$ to $(0,2)$, has relative size $\|(-1, 1)\| / \|(1, 1)\| = 1$: a 100 percent error, close to the worst case. Almost all of the damage comes from the part of $\delta b$ that lies along the direction $A$ squashes most, which $A^{-1}$ stretches by $1/\sigma_{\min} \approx 20{,}000$.

## 8. Low-rank approximation explains puzzle 2

Keep only the first $k$ terms of the SVD sum: $A_k = \sum_{i=1}^{k} \sigma_i u_i v_i^\top$. Because the pieces $u_i v_i^\top$ are orthonormal in the Frobenius inner product, the squared Frobenius norm of $A$ is $\|A\|_F^2 = \sum_i \sigma_i^2$, and the error is

$$
\|A - A_k\|_F^2 = \sum_{i > k} \sigma_i^2 .
$$

**Eckart-Young theorem.** No matrix of rank at most $k$ is closer to $A$, in Frobenius or spectral norm, than $A_k$. (The proof uses the fact that any rank-$k$ matrix has a null space of dimension $n - k$, which must intersect the span of $v_1, \dots, v_{k+1}$; on that intersection $A$ stretches by at least $\sigma_{k+1}$. You will check the statement numerically against random and gradient-trained competitors rather than prove it in full.)

:::edge{to=L20 text="LoRA adapts a model by adding a low-rank update; Eckart-Young says what the best such update can capture."}
:::

**PCA.** Center the data, $X_c = X - \mathbf{1}\mu^\top$, where $\mu$ is the mean row. The variance of the data along a unit direction $w$ is $\dfrac{1}{n-1}\|X_c w\|^2 = w^\top C w$ with covariance $C = \dfrac{X_c^\top X_c}{n-1}$. Maximizing a Rayleigh quotient, the best direction is the top eigenvector of $C$. With the SVD $X_c = U \Sigma V^\top$:

::::derivation{id=d8 title="PCA is the SVD of centered data"}
:::step
$C = \dfrac{X_c^\top X_c}{n-1} = \dfrac{V \Sigma^2 V^\top}{n-1}$. So the principal directions are the columns of $V$, and the variance along $v_i$ is [[s^2/(n-1)]], writing $s$ for $\sigma_i$.
:::
:::step
The **explained variance ratio** of component $i$ is $\sigma_i^2 / \sum_j \sigma_j^2$. If the singular values are $3, 2, 1$ and nothing else, the first component explains $9 / 14 \approx$ [[0.643]] of the variance.
:::
:::step
The coordinates of the data in the new basis, the **scores**, are $X_c V = U \Sigma$. Keeping $k$ columns compresses each $d$-dimensional point into $k$ numbers. For $d = 64$ and $k = 3$, the compression factor per point is [[64/3]].
:::
::::

Embedding clouds are thin pancakes because a few directions have large $\sigma_i$ and the rest have small ones. Puzzle 1 is about the smallest singular value (how close $A$ is to losing rank); puzzle 2 is about the largest ones (where the data actually varies). Same decomposition, opposite ends.

:::edge{to=L13 text="Attention computes dot products between projected token vectors; the geometry here is what those projections do."}
:::

:::aside[Why the Frobenius norm is the sum of squared singular values]
The Frobenius norm satisfies $\|A\|_F^2 = \operatorname{tr}(A^\top A)$, and the trace is invariant under orthogonal changes of basis: $\operatorname{tr}(A^\top A) = \operatorname{tr}(V \Sigma^2 V^\top) = \operatorname{tr}(\Sigma^2 V^\top V) = \sum_i \sigma_i^2$.
:::

## Summary

| Idea | Formula | Where it comes back |
| --- | --- | --- |
| Projection | $P = A(A^\top A)^{-1}A^\top$ | least squares, attention values |
| Normal equations | $A^\top A x = A^\top b$ | linear regression (L05) |
| QR | $A = QR$, solve $Rx = Q^\top b$ | stable least squares |
| Spectral theorem | $S = V \Lambda V^\top$ | PCA, Hessians (L09) |
| SVD | $A = U \Sigma V^\top$ | PCA, low rank, LoRA (L20) |
| Condition number | $\kappa = \sigma_{\max} / \sigma_{\min}$ | optimization speed (L09), mixed precision (L17) |
