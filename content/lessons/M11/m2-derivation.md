# Derivation: elimination, LU and rank

## 1. Row operations

Three operations on the equations of a system do not change its solutions, because each can be undone:

1. add a multiple of one equation to another;
2. swap two equations;
3. multiply an equation by a nonzero number.

**Gaussian elimination** uses the first to clear the entries below the diagonal, one column at a time. In column 1, pick a **pivot**, a nonzero entry, and subtract multiples of its row from the rows below until column 1 is zero under it. Then do the same in column 2 with the rows below the first, and so on. The result is an **upper triangular** system $Ux = c$, solved from the bottom up by **back substitution**.

::::derivation{id=d1 title="One round of elimination"}
:::step
In $\begin{pmatrix} 2 & 1 & -1 \\ -3 & -1 & 2 \\ -2 & 1 & 2 \end{pmatrix}$, clearing the $-3$ under the pivot 2 subtracts $\ell_{21}$ times row 1 from row 2, with multiplier $\ell_{21} = -3/2 =$ [[-1.5]].
:::
:::step
Row 2 becomes $(-3, -1, 2) - (-1.5)(2, 1, -1) = (0, 0.5, 0.5)$. Clearing row 3 uses the multiplier $\ell_{31} =$ [[-1]].
:::
:::step
Each multiplier is the entry to clear divided by the pivot. Row 3 becomes $(0, 2, 1)$. The next pivot is $0.5$, and the multiplier that clears the 2 below it is [[4]].
:::
::::

## 2. Elimination is a factorization: A = LU

Each step "subtract $\ell$ times row $j$ from row $i$" is multiplication on the left by a matrix that differs from the identity by $-\ell$ in position $(i, j)$. Undoing all the steps in reverse order turns $U$ back into $A$, and the matrix that does that has a remarkable form: it is lower triangular, with ones on the diagonal and **the multipliers themselves** below it. So

$$
A = LU, \qquad L = \begin{pmatrix} 1 & 0 & 0 \\ \ell_{21} & 1 & 0 \\ \ell_{31} & \ell_{32} & 1 \end{pmatrix} .
$$

Solving $Ax = b$ then takes two triangular solves: $Ly = b$ from the top down (**forward substitution**), then $Ux = y$ from the bottom up. Factoring costs about $\frac{2}{3} n^3$ operations; each triangular solve about $n^2$. With many right-hand sides, factor once and reuse $L$ and $U$.

::::derivation{id=d2 title="Reading L off the elimination"}
:::step
For the matrix of d1, the multipliers were $\ell_{21} = -1.5$, $\ell_{31} = -1$ and $\ell_{32} = 4$. The entry of $L$ in row 3, column 2 is [[4]].
:::
:::step
$U = \begin{pmatrix} 2 & 1 & -1 \\ 0 & 0.5 & 0.5 \\ 0 & 0 & -1 \end{pmatrix}$. Row 3 of $LU$ is $-1 \cdot (\text{row 1 of } U) + 4 \cdot (\text{row 2}) + 1 \cdot (\text{row 3})$, whose first entry is [[-2]], matching $A$.
:::
:::step
$\det A = \det L \cdot \det U$, and $\det L = 1$, so $\det A$ is the product of the pivots: $2 \cdot 0.5 \cdot (-1) =$ [[-1]].
:::
::::

## 3. Pivoting

Elimination needs a nonzero pivot. If the entry in the pivot position is zero, swap in a row from below that has a nonzero entry there. On paper any nonzero pivot will do. In floating point a **tiny** pivot is a disaster: the multipliers are huge, and adding huge multiples of one row to another wipes out the information in the smaller row.

**Partial pivoting** always swaps up the row with the largest entry, in absolute value, in the current column. Then every multiplier has $|\ell| \leq 1$. The swaps are recorded in a permutation matrix $P$, and the factorization becomes $PA = LU$. Every library solver does this.

::::derivation{id=d3 title="Why a tiny pivot destroys the answer"}
:::step
Solve $10^{-20} x_1 + x_2 = 1$ and $x_1 + x_2 = 2$ without swapping. The multiplier is $10^{20}$, and row 2 becomes $(1 - 10^{20})\,x_2 = 2 - 10^{20}$. In floating point $1 - 10^{20}$ rounds to $-10^{20}$, so $x_2$ comes out as exactly [[1]].
:::
:::step
Back substitution gives $x_1 = (1 - x_2) / 10^{-20} =$ [[0]], while the true $x_1$ is very close to 1.
:::
:::step
With pivoting the rows swap, the multiplier is $10^{-20}$, and both unknowns come out correct to every digit. The largest possible multiplier with partial pivoting has absolute value [[1]].
:::
::::

## 4. Column space, null space and rank

The **column space** of an $m \times n$ matrix $A$ is the set of all $Ax$: every combination of its columns (M10). $Ax = b$ has a solution exactly when $b$ is in it. The **null space** is the set of $x$ with $Ax = 0$, the inputs that $A$ cannot see.

Vectors are **linearly independent** if no one of them is a combination of the others; equivalently, the only combination giving 0 is the one with all weights 0. A **basis** of a space is an independent set that spans it, and every basis of a space has the same number of vectors, its **dimension**.

The **rank** of $A$ is the dimension of its column space. Elimination computes it: row operations do not change which combinations of the columns vanish, so the pivot columns of $U$ mark a basis among the columns of $A$, and **the rank is the number of pivots**. Since row operations also keep the span of the rows, the same count is the dimension of the row space: row rank equals column rank.

## 5. Rank-nullity, and how many solutions

After elimination, each column is either a pivot column or a **free** column. Give each free variable any value and back substitution fixes the pivot variables. So the null space has one dimension per free column:

$$
\operatorname{rank}(A) + \dim \operatorname{null}(A) = n .
$$

This is the **rank-nullity theorem**: of the $n$ input directions, $\operatorname{rank}(A)$ are seen and the rest vanish.

::::derivation{id=d4 title="Counting solutions"}
:::step
The sensor matrix of the puzzle has rank 2 and 3 columns, so its null space has dimension [[1]].
:::
:::step
A $5 \times 8$ matrix has rank at most 5, so its null space has dimension at least [[3]]: eight unknowns and five equations always leave freedom.
:::
:::step
If $x_p$ is one solution of $Ax = b$, every solution is $x_p + z$ with $z$ in the null space, since $A(x_p + z) = b + 0$. So a consistent system with a nonzero null space has [[word:infinitely many/infinite]] solutions.
:::
::::

Altogether, for $Ax = b$:

| Situation | Solutions |
| --- | --- |
| $b$ not in the column space (a zero row of $U$ meets a nonzero entry of $c$) | none |
| $b$ in the column space, rank $= n$ | exactly one |
| $b$ in the column space, rank $< n$ | infinitely many: $x_p$ plus the null space |

For a square matrix, rank $n$ is the same as $\det A \neq 0$, the same as invertible.

## 6. Rank in floating point

On a computer, exact zeros rarely survive. A row that should vanish comes out as $10^{-16}$. So numerical rank counts pivots, or later singular values (M14), above a **tolerance**, usually about $\max(m, n) \cdot \varepsilon \cdot \max |a_{ij}|$ with $\varepsilon \approx 2.2 \times 10^{-16}$. Choose it too small and rounding noise counts as information; too large and a real but small direction is thrown away.

::::derivation{id=d5 title="Choosing a tolerance"}
:::step
For a $1000 \times 1000$ matrix with entries of size about 1, the default tolerance is about $1000 \times 2.2 \times 10^{-16} \approx$ [[2.2e-13|tol=1e-14]].
:::
:::step
A pivot of $10^{-10}$ is far above that, so it counts toward the rank. If the data were only measured to 3 significant digits, a sensible tolerance would be nearer $10^{-3}$, and that pivot would be treated as [[0]].
:::
::::

:::edge{to=M12 text="when b is not in the column space, least squares finds the nearest point that is."}
:::

:::edge{to=M26 text="pivoting returns as a question of numerical stability, measured by the growth of entries and the condition number."}
:::

## Summary

| Idea | Statement | Use |
| --- | --- | --- |
| Elimination | row operations to upper triangular $U$ | solve any system |
| LU | $PA = LU$, $L$ holds the multipliers | factor once, solve many times |
| Partial pivoting | largest entry as pivot, $\lvert \ell \rvert \leq 1$ | stability in floating point |
| Rank | number of pivots; dim of column space and of row space | independent information |
| Rank-nullity | $\operatorname{rank} + \dim \operatorname{null} = n$ | count free parameters |
| Solutions | none, one, or $x_p$ + null space | diagnose a system |
