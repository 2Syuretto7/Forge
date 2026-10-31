# Derivation: the singular value decomposition

## 1. The SVD from the eigenvectors of A^T A

Let $A$ be $m \times n$. $A^\top A$ is $n \times n$ and symmetric, so by the spectral theorem $A^\top A = V\Lambda V^\top$ with orthonormal eigenvectors $v_1, \dots, v_n$, ordered so that $\lambda_1 \geq \lambda_2 \geq \dots$. Each eigenvalue is a squared length: $\lambda_i = v_i^\top A^\top A v_i = \|Av_i\|^2 \geq 0$. Define

$$
\sigma_i = \sqrt{\lambda_i}, \qquad u_i = \frac{Av_i}{\sigma_i} \quad (\sigma_i > 0) .
$$

The $u_i$ are orthonormal: $u_i \cdot u_j = v_i^\top A^\top A v_j / (\sigma_i\sigma_j) = \lambda_j\, v_i \cdot v_j / (\sigma_i\sigma_j)$, which is 1 when $i = j$ and 0 otherwise. By construction $Av_i = \sigma_i u_i$, and in matrix form

$$
A = U\Sigma V^\top = \sum_i \sigma_i\, u_i v_i^\top .
$$

The $\sigma_i$ are the **singular values**, the $v_i$ the right and the $u_i$ the left **singular vectors**. The number of nonzero $\sigma_i$ is the rank.

::::derivation{id=d1 title="An SVD by hand"}
:::step
For $A = \begin{pmatrix} 3 & 0 \\ 4 & 5 \end{pmatrix}$, $A^\top A = \begin{pmatrix} 25 & 20 \\ 20 & 25 \end{pmatrix}$, with eigenvalues $25 \pm 20$. The larger is [[45]].
:::
:::step
So $\sigma_1 = \sqrt{45} \approx 6.71$ and $\sigma_2 = \sqrt 5 \approx 2.24$. Their product is $\sqrt{225} =$ [[15]], which is $|\det A|$: the area factor is the product of the stretches.
:::
:::step
$v_1 = (1, 1)/\sqrt 2$, and $u_1 = Av_1 / \sigma_1 = (3, 9)/(\sqrt 2 \sqrt{45})$. Its first coordinate, $3/\sqrt{90}$, is about [[0.316|tol=0.002]].
:::
::::

## 2. Rotate, stretch, rotate

Read $A = U\Sigma V^\top$ from the right: $V^\top$ is a rotation (perhaps with a reflection) that turns the $v_i$ onto the coordinate axes; $\Sigma$ stretches axis $i$ by $\sigma_i$; $U$ turns the axes onto the $u_i$. So **every** linear map is a rotation, a stretch along perpendicular axes, and another rotation. The unit sphere becomes an ellipsoid with semi-axes $\sigma_i u_i$.

::::predict{id=p3 kind=choice answer=b}
What is the image of the unit circle under a 2 by 2 matrix, in general?

- Always a circle, possibly larger.
- An ellipse, possibly flattened to a segment or a point.
- A parallelogram.
- Any convex shape, depending on the entries.

:::reveal
An ellipse with semi-axes $\sigma_1$ and $\sigma_2$, flattened to a segment when $\sigma_2 = 0$ (rank 1) and to a point for the zero matrix. The parallelogram is the image of the unit square, not of the circle. M10's widget showed this ellipse; its axes are the singular vectors.
:::
::::

The widget shows $0.4A$, scaled to fit. The dashed arrows are $v_1$ and $v_2$, perpendicular inputs, and the solid ones are $\sigma_1 u_1$ and $\sigma_2 u_2$, the perpendicular axes of the ellipse they map to. Change any entry: the two pairs stay perpendicular.

:::widget{name=MatrixTransform a=1.2 b=0 c=1.6 d=2}
:::

The largest stretch, $\sigma_1 = \max_{\|x\| = 1} \|Ax\|$, is the **spectral norm** $\|A\|_2$. The **condition number** of a square invertible $A$ is

$$
\kappa(A) = \frac{\sigma_{\max}}{\sigma_{\min}} ,
$$

the ratio of the longest to the shortest axis. Solving $Ax = b$ can amplify relative errors in $b$ by up to $\kappa$: choose $b$ along $u_1$ (so $\|x\|$ is as small as possible) and the error along $u_n$ (which $A^{-1}$ stretches by $1/\sigma_{\min}$). And since $A^\top A$ has singular values $\sigma_i^2$, $\kappa(A^\top A) = \kappa(A)^2$, the fact M12 used.

::::derivation{id=d2 title="Areas and conditioning from singular values"}
:::step
A 2 by 2 matrix with singular values 4 and $0.5$ multiplies areas by [[2]].
:::
:::step
Its condition number is [[8]], and that of $A^\top A$ is 64.
:::
::::

## 3. Low-rank approximation: Eckart-Young

Cut the sum after $k$ terms: $A_k = \sum_{i \leq k} \sigma_i u_i v_i^\top$. Its error is the rest of the sum, and because the pieces are orthogonal,

$$
\|A - A_k\|_F^2 = \sigma_{k+1}^2 + \dots + \sigma_r^2, \qquad \|A - A_k\|_2 = \sigma_{k+1} .
$$

The **Eckart-Young theorem** says no matrix of rank $k$ does better, in either norm. Truncating the SVD is the best possible compression of a matrix into $k$ rank-one pieces, stored as $k(m + n + 1)$ numbers instead of $mn$.

::::derivation{id=d3 title="Errors of truncation"}
:::step
A matrix with singular values 5, 3 and 1 has $\|A\|_F^2 = 25 + 9 + 1 = 35$. Its best rank-one approximation has Frobenius error [[sqrt(10)]].
:::
:::step
Its best rank-two approximation has spectral-norm error [[1]].
:::
::::

## 4. PCA is the SVD of centred data

Put $n$ data points as the rows of $X$ ($n \times d$), subtract the mean of each column to get $X_c$, and take $X_c = U\Sigma V^\top$. The covariance matrix is

$$
C = \frac{1}{n - 1} X_c^\top X_c = V \frac{\Sigma^2}{n - 1} V^\top ,
$$

so the right singular vectors are the eigenvectors of the covariance, the **principal components**, and $\sigma_i^2/(n-1)$ is the variance of the data along $v_i$. The **scores** $X_c v_i = \sigma_i u_i$ are the coordinates of the points along the components. Keeping $k$ components keeps the fraction $\sum_{i \leq k} \sigma_i^2 / \sum_i \sigma_i^2$ of the variance, and by Eckart-Young the reconstruction from them is the best rank-$k$ fit to the centred data.

::::derivation{id=d4 title="Variance along the components"}
:::step
With $n = 101$ points and top singular value $\sigma_1 = 30$, the variance along the first component is $900 / 100 =$ [[9]].
:::
:::step
With singular values 30, 20 and 10, the first component explains the fraction [[9/14]] of the variance.
:::
::::

## 5. The pseudo-inverse

Invert what can be inverted: $A^+ = V\Sigma^+U^\top$, where $\Sigma^+$ replaces each nonzero $\sigma_i$ by $1/\sigma_i$ and leaves zeros alone. Then $x^+ = A^+ b$ is the least-squares solution of $Ax \approx b$, and among all least-squares solutions it is the one of **smallest length**: it has no component in the null space. For full column rank it agrees with M12's normal equations; when the columns are dependent, where QR and the normal equations fail, it still answers. In floating point, singular values below a tolerance are treated as zero, just as in M11.

::::derivation{id=d5 title="One equation, two unknowns"}
:::step
$x_1 + x_2 = 2$ has the solutions $(1 + t, 1 - t)$. The squared length $(1 + t)^2 + (1 - t)^2 = 2 + 2t^2$ is smallest at $t =$ [[0]].
:::
:::step
For $A = \begin{pmatrix} 1 & 1 \end{pmatrix}$, $\sigma_1 = \sqrt 2$, $v_1 = (1, 1)/\sqrt 2$ and $u_1 = 1$, so $A^+ = v_1 \sigma_1^{-1} u_1^\top$ has both entries equal to [[0.5]], and $A^+ \cdot 2 = (1, 1)$.
:::
::::

:::edge{to=M23 text="PCA is the eigen-decomposition of the covariance matrix; M23 adds the probability."}
:::

:::edge{to=L16 text="LoRA adds a low-rank update to a weight matrix, the object Eckart-Young describes."}
:::

## Summary

| Idea | Statement | Use |
| --- | --- | --- |
| SVD | $A = U\Sigma V^\top$, $\sigma_i = \sqrt{\lambda_i(A^\top A)}$ | every matrix, any shape |
| Geometry | rotate, stretch, rotate; sphere to ellipsoid | read any map |
| Norms | $\|A\|_2 = \sigma_1$, $\|A\|_F^2 = \sum \sigma_i^2$ | sizes of matrices |
| Condition number | $\kappa = \sigma_{\max}/\sigma_{\min}$, $\kappa(A^\top A) = \kappa^2$ | digits lost |
| Eckart-Young | $A_k$ is the best rank $k$; error from the tail | compression, LoRA |
| PCA | SVD of centred data; variance $\sigma_i^2/(n-1)$ | find the important directions |
| Pseudo-inverse | $A^+ = V\Sigma^+U^\top$, minimal-length least squares | dependent columns |
