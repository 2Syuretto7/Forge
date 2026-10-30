# Determinants too large to store

The determinant of a $300 \times 300$ matrix with entries of size 10 is around $10^{600}$: it overflows a float64. Its logarithm does not.

- `logabsdet(A)`: return `(sign, log|det A|)` from LU with partial pivoting (the starter provides `lu`): the sign of the permutation times the signs of the pivots, and the sum of the logarithms of the absolute pivots. A zero pivot gives `(0, -inf)`.
- `naive_det(A)`: the product of the pivots times the permutation's sign, which overflows.

## Hints

1. `np.sum(np.log(np.abs(np.diag(U))))`.
2. Count the sign flips: one per row swap and one per negative pivot.
3. Compare with `np.linalg.slogdet`.
