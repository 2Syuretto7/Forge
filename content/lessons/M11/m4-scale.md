# Scale: a thousand equations

An $n \times n$ LU costs about $\frac{2}{3}n^3$ operations: for $n = 1000$, about $6.7 \times 10^8$. Written with one vectorized row update per pivot, NumPy performs that in a second or so; LAPACK, which `np.linalg.solve` calls, does it in milliseconds by working in blocks.

::::predict{id=p3 kind=choice answer=b}
You need to solve $Ax = b$ for 100 different right-hand sides $b$ with the same $1000 \times 1000$ matrix. Which is cheapest?

- Run elimination from scratch 100 times.
- Factor $A = LU$ once, then do 100 pairs of triangular solves.
- Compute $A^{-1}$ and multiply it by each $b$.
- All three cost about the same.

:::reveal
Factor once: $\frac{2}{3}n^3$ for the factorization plus $100 \times 2n^2$ for the solves, about $8.7 \times 10^8$ operations. Elimination from scratch costs $100 \times \frac{2}{3}n^3 \approx 6.7 \times 10^{10}$. Forming the inverse costs about $2n^3$ and is less accurate as well. Libraries expose the factorization separately for this reason.
:::
::::

:::exercise{ref=e10}
:::

:::exercise{ref=e11}
:::

:::exercise{ref=e12}
:::

The widget's tiny leading entry is the whole story of pivoting in two equations. Turn pivoting off and watch the residual.

:::widget{name=EliminationStepper preset=tiny pivoting=false}
:::
