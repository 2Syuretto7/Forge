# Build: the toolkit from scratch

Time to turn every derivation into code. Nine exercises, each a small module checked by hidden tests. The tests check values against NumPy, shapes, invariants such as $Q^\top Q = I$ and $P^2 = P$, and, where a gradient exists, your gradient against central finite differences at a relative error below $10^{-5}$.

Work in order: later exercises reuse ideas, not code, so each module is self-contained.

## Measuring vectors

Everything starts with dot products. Write them with elementwise operations once, so you know there is nothing magic inside `@`.

:::exercise{ref=e01}
:::

## Projections

Section 2 and 3 of the derivation, in code. The tests check the two algebraic fingerprints of an orthogonal projection: symmetry and idempotence.

:::exercise{ref=e02}
:::

## Orthonormal bases

Gram-Schmidt is where numerical analysis first bites. Implement the modified form; one test feeds you nearly parallel columns.

:::exercise{ref=e03}
:::

::::predict{id=p4 kind=choice answer=b}
You run classical Gram-Schmidt on a matrix with condition number $10^7$ in float64 ($\varepsilon \approx 10^{-16}$). Roughly how far from the identity is $Q^\top Q$?

- About $10^{-16}$, rounding level.
- About $10^{-5}$ to $10^{-2}$: classical Gram-Schmidt loses orthogonality roughly like $\kappa^2 \varepsilon$.
- About $1$: the columns come out completely non-orthogonal.

:::reveal
The classical update computes all coefficients from the original column, so rounding errors in early $q_j$ are never corrected; the loss of orthogonality grows like $\kappa^2 \varepsilon \approx 10^{-2}$ in the worst case and is often a little smaller in practice (the exercise's test matrix gives about $2 \times 10^{-5}$). The modified form recomputes each coefficient from the partially orthogonalized vector and its error grows only like $\kappa \varepsilon \approx 10^{-9}$.
:::
::::

:::exercise{ref=e04}
:::

## Least squares

Now the main event of Section 3: two solvers and a report that verifies the geometry of the answer.

:::exercise{ref=e05}
:::

The same problem, solved by walking downhill. This is your first gradient check; you will write dozens more in this course, and they all look like this one.

:::exercise{ref=e06}
:::

## Eigenvectors

Power iteration is three lines of code; the interesting part is predicting how many iterations it needs.

:::exercise{ref=e07}
:::

:::exercise{ref=e08}
:::

## The SVD

The construction of Section 6, line by line. Pay attention to the rank threshold: it is the first sign of the squaring problem you will break things with in Movement 5.

:::exercise{ref=e09}
:::
