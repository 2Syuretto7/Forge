# A basis for the null space

`null_space(A, tol=1e-10)` returns an `(n, n - r)` array whose columns are a basis of the null space: for each free column of the reduced row echelon form, set that free variable to 1, the other free variables to 0, and read the pivot variables off $R$. The starter provides `rref`.

The tests check an **invariant**, the rank-nullity theorem: for random matrices of known rank, the basis has $n - r$ columns, $AN \approx 0$, and the columns are independent.

## Hints

1. Free columns are those not in `pivots`.
2. With free variable $f$ set to 1, pivot variable `pivots[i]` equals `-R[i, f]`.
3. A matrix of full rank returns an array of shape `(n, 0)`.
