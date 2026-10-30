# The matrix-vector product, two ways

Matrices here are lists of rows (plain Python lists, no NumPy).

- `matvec_rows(A, x)`: output $i$ is the dot product of row $i$ with `x`.
- `matvec_cols(A, x)`: the combination $x_1 (\text{column } 1) + \dots + x_n (\text{column } n)$, built column by column.
- Both raise `ValueError` when the row length of `A` differs from `len(x)`.

The tests check an **invariant**: the two agree, and the product is linear, $A(a x + b y) = a\,Ax + b\,Ay$, for random matrices and vectors.

## Hints

1. `sum(a * b for a, b in zip(row, x))`.
2. Start from a list of zeros of length $m$ and add `x[j]` times column `j`.
3. Column `j` is `[row[j] for row in A]`.
