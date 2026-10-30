# Triangular solves

- `forward_sub(L, b)`: solve $Ly = b$ for a lower triangular NumPy array `L`, from the top row down.
- `back_sub(U, c)`: solve $Ux = c$ for an upper triangular `U`, from the bottom row up.
- Both raise `ValueError` if a diagonal entry is exactly 0.

Use loops over rows; inside a row, a dot product with the part already solved is allowed. The tests check an **invariant**: for random triangular matrices with diagonals away from 0, the solutions satisfy their systems to rounding.

## Hints

1. Row $i$ of $Ly = b$ says $L_{ii} y_i = b_i - \sum_{j < i} L_{ij} y_j$.
2. `L[i, :i] @ y[:i]` is that sum.
3. Loop `for i in range(n - 1, -1, -1)` for back substitution.
