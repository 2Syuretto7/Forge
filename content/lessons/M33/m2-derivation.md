# Derivation: numerical linear algebra at scale

## 1. Flops, bytes and the roofline

Count two things for every kernel: the floating-point operations it performs and the bytes it must move between memory and the processor. Their ratio is the **arithmetic intensity** $I$, in flops per byte. A chip with peak $P$ flops per second and memory bandwidth $W$ bytes per second runs the kernel at most at

$$
\min(P,\ I\cdot W)
$$

flops per second: the **roofline**. The two roofs meet at the **ridge point** $I^* = P/W$. Below it a kernel is **memory-bound** and its speed is $I\cdot W$; above it, **compute-bound** at $P$. For a T4 in fp32, $I^* = 8.1 \times 10^{12}/3.2 \times 10^{11} \approx 25$ flops per byte.

| Kernel | Flops | Words moved | Intensity (fp32) |
| --- | --- | --- | --- |
| $x + y$, length $n$ | $n$ | $3n$ | $1/12$ |
| $Ax$, $n \times n$ | $2n^2$ | $n^2 + 2n$ | $\approx 1/2$ |
| $AB$, $n \times n$ | $2n^3$ | $3n^2$ | $n/6$ |

::::derivation{id=d1 title="The 4096 product"}
:::step
$2 \times 4096^3 \approx$ [[137.4|tol=0.1]] billion flops.
:::
:::step
The minimal traffic, $3 \times 4096^2$ numbers of 4 bytes, is about [[201|tol=1]] million bytes.
:::
:::step
So the intensity is about [[683|tol=1]] flops per byte, far above the T4's ridge point.
:::
::::

Move the intensity and watch which roof limits the kernel.

:::widget{name=Roofline hardware=t4 precision=fp32}
:::

:::edge{to=L07 text="arithmetic intensity places each GPU kernel on the roofline."}
:::

## 2. Blocking: reuse what you read

The minimal traffic is reachable only if each number, once fetched, is used many times before it is evicted. Model the memory as a fast cache holding $M$ words in front of a slow memory. The textbook loop computes $C_{ij}$ from a row of $A$ and a column of $B$, $2n$ words per output, $2n^3$ in all. The **blocked** algorithm splits the matrices into $b \times b$ tiles and computes each output tile as a sum of $n/b$ tile products. With three tiles in cache, $3b^2 \le M$, each tile product reads $2b^2$ words and does $2b^3$ flops, so the traffic falls to

$$
\frac{2n^3}{b} + n^2
$$

words, $b$ times less, and the intensity rises by the same factor. Hong and Kung proved that no ordering of the standard algorithm can move fewer than order $n^3/\sqrt M$ words, so blocking with $b \approx \sqrt{M/3}$ is optimal up to a constant. Real libraries block for every level of the hierarchy, registers, caches and GPU shared memory, which is how they reach 80 to 90 percent of peak.

::::derivation{id=d2 title="A tile for a 32 KB cache"}
:::step
A cache of 8,192 fp32 words holds three $b \times b$ tiles for $b$ up to [[52]].
:::
:::step
That cuts the traffic of the triple loop by a factor of about [[52]].
:::
::::

## 3. Conjugate gradient and Krylov subspaces

Some matrices are too large to factor, or are never stored at all: only the product $v \mapsto Av$ is available. For a symmetric positive definite $A$, solving $Ax = b$ is minimizing $f(x) = \frac12x^\top Ax - b^\top x$, since $\nabla f = Ax - b$. Steepest descent zig-zags. **Conjugate gradient** chooses directions that are **$A$-orthogonal**, $p_i^\top Ap_j = 0$ for $i \ne j$; then minimizing along each in turn never spoils the earlier minimizations, and

$$
\alpha_k = \frac{r_k^\top r_k}{p_k^\top Ap_k}, \qquad p_{k+1} = r_{k+1} + \frac{r_{k+1}^\top r_{k+1}}{r_k^\top r_k}\,p_k
$$

make each new direction conjugate to all the previous ones with only the last one stored. After $k$ steps, $x_k$ is the minimizer of $f$ over the **Krylov subspace** $\mathcal K_k = \mathrm{span}\{b, Ab, \dots, A^{k-1}b\}$. The error is therefore $q(A)e_0$ for the best polynomial $q$ of degree $k$ with $q(0) = 1$, and two facts follow. If $A$ has $d$ distinct eigenvalues, a polynomial with those $d$ roots exists, and CG finishes in $d$ steps. In general, Chebyshev polynomials on $[\lambda_{\min}, \lambda_{\max}]$ give

$$
\frac{\lVert e_k\rVert_A}{\lVert e_0\rVert_A} \le 2\left(\frac{\sqrt\kappa - 1}{\sqrt\kappa + 1}\right)^k ,
$$

about $\frac12\sqrt\kappa\ln(2/\varepsilon)$ steps to reach accuracy $\varepsilon$, against about $\frac12\kappa\ln(1/\varepsilon)$ for gradient descent (M29).

::::derivation{id=d3 title="CG at condition number ten thousand"}
:::step
With $\kappa = 10^4$ the error shrinks per step by at most $(100 - 1)/(100 + 1) \approx$ [[0.980|tol=0.001]].
:::
:::step
To reach $10^{-8}$ the bound needs $\lceil\ln(2 \times 10^8)/\ln(101/99)\rceil =$ [[956|tol=2]] steps; gradient descent would need about a hundred times more.
:::
::::

::::predict{id=p3 kind=numeric answer=5 tol=0}
A $200 \times 200$ symmetric positive definite matrix has only five distinct eigenvalues, each repeated 40 times. How many CG iterations solve $Ax = b$ to a relative residual of $10^{-10}$?

:::reveal
Five. The polynomial with roots at the five eigenvalues, scaled so that $q(0) = 1$, annihilates the error, and CG finds the best polynomial of each degree. The dimension, 200, does not matter; the number of distinct eigenvalues does. You will see it happen in e05.
:::
::::

## 4. Preconditioning

If $\kappa$ is the obstacle, change it. For a symmetric positive definite $M \approx A$ that is cheap to invert, CG on the equivalent system with matrix $M^{-1/2}AM^{-1/2}$ converges at the rate of its condition number, and the algorithm needs only products with $A$ and solves with $M$. The **Jacobi** preconditioner $M = \mathrm{diag}(A)$ removes bad scaling of the variables: if $A = DA_0D$ with $D$ diagonal and $A_0$ well conditioned, $\kappa(A)$ can be as large as $\kappa(A_0)$ times the square of $D$'s spread, while Jacobi brings it back close to $\kappa(A_0)$. Incomplete factorizations and multigrid do the same for harder structure. Regularization helps too: ridge regression's $X^\top X + \lambda I$ has condition number at most $(\sigma_1^2 + \lambda)/\lambda$.

## 5. Randomized range finders and the randomized SVD

To approximate $A$ ($m \times n$) at rank $k$, first find a basis for its dominant column space. Multiply by a Gaussian matrix $\Omega$ of shape $n \times (k + p)$: each column of $Y = A\Omega = \sum_j\sigma_ju_j(v_j^\top\Omega)$ weights $u_j$ by $\sigma_j$ times a random coefficient, so the top directions dominate. Orthonormalize, $Q = \mathrm{qr}(Y)$, then compress, $B = Q^\top A$, a small $(k + p) \times n$ matrix whose SVD $B = \tilde U\Sigma V^\top$ gives $A \approx (Q\tilde U)\Sigma V^\top$. Halko, Martinsson and Tropp proved, with $p \ge 2$ extra columns of **oversampling**,

$$
\mathbb{E}\lVert A - QQ^\top A\rVert_F \le \sqrt{1 + \frac k{p - 1}}\ \Big(\sum_{j > k}\sigma_j^2\Big)^{1/2} ,
$$

a small constant times the Eckart-Young optimum (M14). When the singular values decay slowly the constant is not the issue; the tail is large and the random combinations mix in too much of it. **Power iterations**, $Y = (AA^\top)^qA\Omega$ with re-orthonormalization between products, replace $\sigma_j$ by $\sigma_j^{2q+1}$ and make the decay steep.

:::edge{to=M34 text="random projections preserve the geometry of a subspace, which is why the range finder works."}
:::

::::derivation{id=d4 title="The oversampling constant"}
:::step
For $k = 10$ and $p = 5$ the expected error is at most $\sqrt{1 + 10/4} \approx$ [[1.871|tol=0.002]] times the optimum.
:::
::::

The cost is $2(q + 1)$ passes over $A$, each a product with $k + p$ columns, plus small factorizations: about $4(q + 1)mn(k + p)$ flops, against order $mn^2$ for a full SVD, and the products run near the compute roof.

## 6. Sketching

The same idea shrinks problems. For tall least squares, $\min_x\lVert Ax - b\rVert$ with $A$ of shape $m \times n$ and $m \gg n$, multiply by a random $S$ of shape $s \times m$ with $N(0, 1/s)$ entries. With high probability $S$ preserves the length of every vector in the $(n + 1)$-dimensional span of $A$'s columns and $b$ to within a factor close to 1, a subspace version of the Johnson-Lindenstrauss lemma that M34 proves. The sketched problem $\min_x\lVert S(Ax - b)\rVert$ is $s \times n$, and its solution's residual is within a factor of about $\sqrt{1 + n/(s - n - 1)}$ of the best. A dense Gaussian sketch costs as much as the original solve; structured sketches (subsampled randomized Fourier transforms, sparse sign matrices) apply in time close to the size of $A$.

## 7. Stability at scale

Speed must not cost accuracy. Least squares through the **normal equations** $A^\top Ax = A^\top b$ is the cheapest method, but $\kappa(A^\top A) = \kappa(A)^2$, so its error is about $\kappa(A)^2\varepsilon$ where QR's is about $\kappa(A)\varepsilon$ (M26). In double precision, with $\varepsilon \approx 10^{-16}$, a polynomial fit with $\kappa(A) = 10^8$ keeps about 8 digits by QR and none by the normal equations. Conjugate gradient on the normal equations (CGNR) inherits the squared condition number in its speed, not in its formation: it never forms $A^\top A$.

::::derivation{id=d5 title="Digits lost"}
:::step
For $\kappa(A) = 10^4$, QR loses about 4 of the 16 digits of double precision; the normal equations, with $\kappa(A^\top A) = 10^8$, lose about [[8]].
:::
::::

:::edge{to=M38 text="low-rank structure and the cost of matrix products in efficient models."}
:::

## Summary

| Idea | Statement | Use |
| --- | --- | --- |
| Roofline | speed $\le \min(P, IW)$; ridge $I^* = P/W$ | memory- or compute-bound |
| Blocking | traffic $2n^3/b + n^2$ with $3b^2 \le M$ | reuse each word $b$ times |
| Conjugate gradient | best point in the Krylov subspace; $\approx\frac12\sqrt\kappa\ln(2/\varepsilon)$ steps | matrix-free solves |
| Preconditioning | rate set by $\kappa(M^{-1}A)$ | fix scaling and structure |
| Randomized SVD | $Q = \mathrm{qr}((AA^\top)^qA\Omega)$, SVD of $Q^\top A$; error $\le\sqrt{1 + k/(p - 1)}\times$ optimum | fast low-rank approximation |
| Sketching | residual within $\approx\sqrt{1 + n/(s - n - 1)}$ | shrink tall problems |
| Normal equations | $\kappa(A^\top A) = \kappa(A)^2$ | use QR, or never form $A^\top A$ |
