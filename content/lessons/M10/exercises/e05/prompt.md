# Determinants and the 2 by 2 inverse

Without `np.linalg`:

- `det2(A)`: $ad - bc$.
- `det3(A)`: expansion along the first row.
- `inverse2(A)`: $\frac{1}{ad - bc}\begin{pmatrix} d & -b \\ -c & a \end{pmatrix}$ as a NumPy array; raise `ValueError` when the determinant is 0.

The tests check an **invariant**: $\det(AB) = \det A \det B$ for random 3 by 3 matrices.

## Hints

1. Unpack `(a, b), (c, d) = A`.
2. Each first-row entry multiplies the 2 by 2 determinant left after deleting its row and column, with signs $+, -, +$.
3. Compare the determinant with exactly 0; a near-singular matrix still has an inverse, just a huge one.
