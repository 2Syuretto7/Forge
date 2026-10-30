# Derivation: projections and least squares

## 1. Orthogonal complements

Two vectors are **orthogonal** when their dot product is 0. A vector is orthogonal to a subspace $V$ when it is orthogonal to every vector of $V$, and it suffices to check a basis. All such vectors form the **orthogonal complement** $V^\perp$, itself a subspace. In $\mathbb{R}^3$ the complement of a plane through the origin is the line along its normal; the complement of that line is the plane.

The complement of the column space of $A$ is the null space of $A^\top$: $z \perp$ every column means $a_j \cdot z = 0$ for each $j$, which is $A^\top z = 0$. By rank-nullity (M11) applied to $A^\top$, the dimensions add up: $\dim V + \dim V^\perp = m$. Every $b \in \mathbb{R}^m$ splits in exactly one way as $b = p + r$ with $p \in V$ and $r \in V^\perp$.

## 2. Projection onto a subspace

Let $V$ be the column space of an $m \times n$ matrix $A$ with independent columns. The **projection** of $b$ onto $V$ is the point $p = A\hat x$ of $V$ nearest to $b$. Drop a perpendicular: the residual $b - A\hat x$ must be orthogonal to every column,

$$
A^\top (b - A\hat x) = 0, \qquad \text{that is} \qquad A^\top A\, \hat x = A^\top b .
$$

These are the **normal equations**: $n$ equations in $n$ unknowns, whatever the number $m$ of data points. $A^\top A$ is invertible when the columns are independent, since $A^\top A x = 0$ gives $x^\top A^\top A x = \|Ax\|^2 = 0$, so $Ax = 0$ and $x = 0$.

::::derivation{id=d1 title="The normal equations of a line fit"}
:::step
Fit $y \approx w_0 + w_1 x$ through points at $x = 0, 1, 2$. The design matrix $A$ has a column of ones and a column $(0, 1, 2)$. The top-left entry of $A^\top A$ is the column of ones dotted with itself: [[3]].
:::
:::step
The off-diagonal entry is $\sum x_i = 3$, and the bottom-right entry is $\sum x_i^2 =$ [[5]].
:::
:::step
With $y = (0, 1, 1)$, $A^\top y = (\sum y_i, \sum x_i y_i) = (2, 3)$. Solving $\begin{pmatrix} 3 & 3 \\ 3 & 5 \end{pmatrix} w = \begin{pmatrix} 2 \\ 3 \end{pmatrix}$ by M02's elimination gives the slope $w_1 =$ [[0.5]].
:::
::::

## 3. Why it is the minimum: Pythagoras, without calculus

Suppose $\hat x$ satisfies the normal equations, and take any other $x = \hat x + d$. Then $Ax - b = (A\hat x - b) + Ad$, and expanding the squared length,

$$
\|Ax - b\|^2 = \|A\hat x - b\|^2 + 2\, d^\top A^\top (A\hat x - b) + \|Ad\|^2 .
$$

::::derivation{id=d2 title="Every other x does worse"}
:::step
By the normal equations, $A^\top (A\hat x - b) = 0$, so the middle term equals [[0]].
:::
:::step
So $\|Ax - b\|^2 = \|A\hat x - b\|^2 + \|Ad\|^2$, Pythagoras for the right triangle with legs $A\hat x - b$ and $Ad$. The excess over the minimum is $\|Ad\|^2$, which is zero only when $Ad = 0$, that is, with independent columns, when $d =$ [[0]].
:::
:::step
The same expansion with $d = t\,u$ for a number $t$ and a direction $u$, at any point $x$ (not only the minimizer), reads $\|A(x + tu) - b\|^2 = \|Ax - b\|^2 + t\, (s \cdot u) + t^2 \|Au\|^2$ with $s = 2A^\top(Ax - b)$. If $s \cdot u = -4$ and $\|Au\|^2 = 1$, the step $t = 0.1$ changes the squared error by [[-0.39]]. For small $t$ the linear term wins, so stepping against $s$ lowers the error; M18 will name $s$ the gradient.
:::
::::

The **projection matrix** sends $b$ to $p$: $P = A (A^\top A)^{-1} A^\top$. It is symmetric, and projecting twice changes nothing, $P^2 = P$.

::::predict{id=p3 kind=choice answer=b}
$P$ projects onto a plane in $\mathbb{R}^3$. What is $P$ applied to the normal vector of the plane, and to a vector already in the plane?

- The normal vector is unchanged; a vector in the plane goes to 0.
- The normal vector goes to 0; a vector in the plane is unchanged.
- Both are scaled by one half.
- Both are unchanged.

:::reveal
The normal vector is perpendicular to the plane, so its nearest point in the plane is the origin: $Pn = 0$. A vector already in the plane is its own nearest point: $Pv = v$. So $P$ has eigenvalues 1 (twice, the plane) and 0 (the normal). M13 makes eigenvalues the main subject.
:::
::::

::::derivation{id=d3 title="Properties of the projection matrix"}
:::step
$P^2 = A(A^\top A)^{-1} A^\top A (A^\top A)^{-1} A^\top$. The middle $A^\top A (A^\top A)^{-1}$ is the identity, so $P^2 = P$. The residual maker $I - P$ also satisfies $(I - P)^2 = I - 2P + P^2 =$ [[word:I - P/I-P/the same matrix]].
:::
:::step
The trace (the sum of the diagonal) satisfies $\operatorname{tr}(MN) = \operatorname{tr}(NM)$, so $\operatorname{tr} P = \operatorname{tr}\big((A^\top A)^{-1} A^\top A\big) = \operatorname{tr}(I_n)$. For a $100 \times 3$ design matrix, $\operatorname{tr} P =$ [[3]].
:::
::::

:::widget{name=VectorPlayground x1=2.5 x2=1 y1=1 y2=2 proj=true}
:::

In two dimensions the subspace is a line, and the dotted segment is the residual, perpendicular to it. Move $y$ anywhere: the right angle stays.

:::edge{to=L05 text="linear regression is this problem; L05 explains why squared error is the natural loss."}
:::

:::edge{to=M22 text="variance is a squared length and covariance an inner product, so fitting and statistics share this geometry."}
:::

:::edge{to=M25 text="least squares is maximum likelihood under Gaussian noise."}
:::

## 4. Orthonormal bases make projection a dot product

If the columns $q_1, \dots, q_n$ of $Q$ are **orthonormal**, unit length and mutually perpendicular, then $Q^\top Q = I$. The normal equations collapse to $\hat x = Q^\top b$: each coefficient is one dot product, $\hat x_j = q_j \cdot b$, and the projection is $P = QQ^\top$.

**Gram-Schmidt** builds an orthonormal basis from any independent $a_1, \dots, a_n$. Take $a_k$, subtract its components along the $q$'s already built, and normalize what is left:

$$
v_k = a_k - \sum_{j < k} (q_j \cdot a_k)\, q_j, \qquad q_k = \frac{v_k}{\|v_k\|} .
$$

Recording the coefficients gives the **QR factorization** $A = QR$: $Q$ has the orthonormal columns, and $R$ is upper triangular with $R_{jk} = q_j \cdot a_k$ for $j < k$ and $R_{kk} = \|v_k\| > 0$.

::::derivation{id=d4 title="Gram-Schmidt in the plane"}
:::step
$a_1 = (3, 4)$ has length 5, so $q_1 = (0.6, 0.8)$. For $a_2 = (1, 0)$ the coefficient is $R_{12} = q_1 \cdot a_2 =$ [[0.6]].
:::
:::step
$v_2 = a_2 - 0.6\, q_1 = (0.64, -0.48)$, whose length is $R_{22} =$ [[0.8]].
:::
:::step
Substituting $A = QR$ into the normal equations, $R^\top Q^\top Q R \hat x = R^\top Q^\top b$, and since $Q^\top Q = I$ and $R^\top$ is invertible, $R\hat x = Q^\top b$: a triangular system, solved by [[word:back substitution/backward substitution/back-substitution]].
:::
::::

In floating point the formula above, **classical** Gram-Schmidt, slowly loses orthogonality when the columns are nearly parallel. The **modified** version subtracts each projection from the running vector at once, recomputing each coefficient from the updated vector. It is the same in exact arithmetic and far better in practice. Libraries use a third method, Householder reflections, which is better still.

## 5. Why QR beats the normal equations

The **condition number** $\kappa(A)$ measures how much $A$ can amplify relative errors (M11 met it as the sensitivity of a nearly singular system; M14 computes it exactly). Solving a least-squares problem loses about $\log_{10} \kappa$ digits by a good method. The normal equations work with $A^\top A$, and $\kappa(A^\top A) = \kappa(A)^2$: they lose twice as many.

::::derivation{id=d5 title="Squaring the condition number"}
:::step
If $\kappa(A) = 10^6$, then $\kappa(A^\top A) =$ [[1e12]].
:::
:::step
Double precision carries about 16 digits. QR loses about 6 and keeps about 10; the normal equations lose about 12 and keep about [[4]].
:::
::::

A polynomial fit with columns $1, x, x^2, \dots, x^{15}$ on $[0, 1]$ has $\kappa(A)$ around $10^{11}$: QR keeps a few digits, and the normal equations, at $\kappa^2 \approx 10^{22}$, keep none.

## Summary

| Idea | Statement | Use |
| --- | --- | --- |
| Complement | $\operatorname{col}(A)^\perp = \operatorname{null}(A^\top)$; dimensions add to $m$ | split $b = p + r$ |
| Normal equations | $A^\top A \hat x = A^\top b$ | least squares, $n$ equations |
| Pythagoras | $\|Ax - b\|^2 = \|A\hat x - b\|^2 + \|A(x - \hat x)\|^2$ | why it is the minimum |
| Projection matrix | $P = A(A^\top A)^{-1}A^\top$, $P^2 = P$, $\operatorname{tr} P = n$ | fitted values, leverage |
| Orthonormal $Q$ | $\hat x = Q^\top b$, $P = QQ^\top$ | cheap, stable projections |
| QR | $A = QR$; solve $R\hat x = Q^\top b$ | least squares with $\kappa(A)$, not $\kappa(A)^2$ |
