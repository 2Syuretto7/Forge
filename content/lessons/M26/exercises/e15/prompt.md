# Break it: elimination without pivoting

Solve $\begin{pmatrix} \delta & 1 \\ 1 & 1\end{pmatrix} x = \begin{pmatrix} 1 \\ 2 \end{pmatrix}$ with $\delta = 10^{-20}$. The exact solution is very close to $(1, 1)$. Gaussian elimination with the tiny pivot $\delta$ multiplies the first row by $10^{20}$, and the information in the second row is rounded away (M11, Section 3).

- `solve_no_pivot(A, b)`: Gaussian elimination and back substitution, always using the diagonal entry as pivot.
- `solve_partial_pivot(A, b)`: the same, but swap in the row with the largest entry in the current column first.
- `growth_factor(A, pivot)`: the largest absolute entry appearing during elimination divided by the largest entry of $A$, with or without pivoting (`pivot` is a boolean).

The tests show the unpivoted solve returning $x_1 = 0$, the pivoted one correct, and the growth factor near $10^{20}$ without pivoting and at most 2 with it.

## Hints

1. Work on float copies: `A = np.array(A, dtype=float)`.
2. For each column $k$: eliminate below with multipliers `A[i, k] / A[k, k]`; track the largest entry after each step.
3. With pivoting, `p = k + np.argmax(np.abs(A[k:, k]))`, then swap rows `k` and `p` of both `A` and `b`.
