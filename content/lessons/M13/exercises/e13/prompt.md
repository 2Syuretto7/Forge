# When no eigenvalue wins

- `power_history(A, x0, k)`: the list of the $k + 1$ unit vectors $x_0, x_1, \dots, x_k$ of power iteration (each normalized).
- `settled(history, tol=1e-8)`: whether the last two vectors point along the same line, $|x_{k-1} \cdot x_k| \geq 1 - \text{tol}$ (a sign flip still counts as settled: a negative dominant eigenvalue flips the vector each step).
- `shifted_top(A, shift, k, x0)`: power iteration on $A + \text{shift}\cdot I$; return the Rayleigh quotient of the final vector **for $A$**, an eigenvalue of $A$.

## Hints

1. Normalize `x0` first.
2. For $\begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$ the iterates alternate between two perpendicular vectors.
3. A shift moves every eigenvalue by the same amount, so it can break a tie in absolute value.
