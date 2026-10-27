# Puzzle: garbage answers and crowded directions

Two observations open this lesson. They look unrelated. By the end of the derivation you will see that both are statements about the same object: the singular values of a matrix.

## Puzzle 1: a system that returns garbage

Consider the system

$$
\begin{aligned}
x_1 + x_2 &= 2 \\
x_1 + 1.0001\,x_2 &= 2.0001
\end{aligned}
$$

Its solution is $x = (1, 1)$; check it. Now nudge the right-hand side of the second equation by $0.0001$, a change of five thousandths of a percent.

::::predict{id=p1 kind=numeric answer=0 tol=0.05}
After changing $2.0001$ to $2.0002$, what is the new value of $x_1$?

:::reveal
Subtracting the first equation from the second gives $0.0001\,x_2 = 0.0002$, so $x_2 = 2$ and $x_1 = 0$. A change of $0.005\%$ in the data moved the answer from $(1,1)$ to $(0,2)$. Nothing is wrong with the arithmetic: the two equations describe two almost parallel lines, and almost parallel lines cross at a point that slides a long way when either line shifts slightly.
:::
::::

Now imagine the same system with a thousand unknowns, entries measured with noise, and arithmetic done in 32-bit floats that keep about seven significant digits. If the problem amplifies errors by a factor of $10^8$, you get no correct digits at all. Later in this lesson you will name that amplification factor (the **condition number**), compute it, and learn which algorithms make it worse.

## Puzzle 2: embeddings live on a few directions

Take 2,000 sentence embeddings from a language model, each a vector in $\mathbb{R}^{768}$. You might expect 768 independent directions of variation. In practice, a handful of directions carry most of the variance: the cloud of points is a thin, tilted pancake rather than a ball.

::::predict{id=p2 kind=choice answer=c}
A synthetic embedding set has 64 dimensions built from 3 underlying factors plus small noise. What fraction of the total variance do you expect the best 3 directions to capture?

- About $3/64 \approx 5\%$, since each direction carries an equal share.
- About $50\%$.
- Well over $90\%$.
- Exactly $100\%$.

:::reveal
If the data really are 3 factors plus small noise, the best 3 directions capture all of the factor variance and only the noise is left over, so the share is well over $90\%$ but not exactly $100\%$. You will verify this in the capstone, and the tool that finds those directions (PCA) is the SVD applied to centered data.
:::
::::

## The common thread

In puzzle 1, the matrix $A = \begin{pmatrix} 1 & 1 \\ 1 & 1.0001 \end{pmatrix}$ squashes some direction almost to zero: there is a vector $v$ with $\|Av\|$ tiny compared with $\|v\|$. Solving $Ax = b$ means undoing that squash, which multiplies any error along that direction by a huge factor.

In puzzle 2, the data matrix $X$ (one embedding per row) stretches a few directions a lot and the rest hardly at all.

Both statements are about how much a matrix stretches different directions. The singular value decomposition lists exactly those stretch factors. Here is a preview with the widget below: drag $d$ toward $b c / a$ and watch one axis of the ellipse collapse.

:::widget{name=MatrixTransform a=1 b=1 c=1 d=1.2}
:::

::::predict{id=p3 kind=sketch answer="1,0.37,0.14,0.05,0.02,0.01" xlabel="rank k kept (0 to 5)" ylabel="relative error"}
A matrix has singular values that fall by a factor of about $e$ each step: $1, e^{-1}, e^{-2}, \dots$. Sketch the relative error $\|A - A_k\|_F / \|A\|_F$ of the best rank-$k$ approximation for $k = 0, \dots, 5$.

:::reveal
The squared error after keeping $k$ terms is the sum of the remaining squared singular values, which here is a geometric series with ratio $e^{-2}$. The relative error is therefore $e^{-k}$: $1, 0.37, 0.14, 0.05, 0.02, 0.007$. Fast singular value decay means a low-rank approximation is nearly exact, which is why images and embeddings compress well.
:::
::::

## Questions to carry into the derivation

1. What is the closest point to $b$ that $Ax$ can reach, when no $x$ solves $Ax = b$ exactly?
2. Which directions does a matrix stretch most and least, and how do we find them?
3. How much can errors in $b$ grow when we solve for $x$?
4. If we keep only the $k$ most important directions, how much do we lose?
