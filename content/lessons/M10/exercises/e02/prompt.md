# Matrix multiplication three ways

For NumPy arrays `A` of shape `(m, n)` and `B` of shape `(n, p)`, compute $AB$ without `@`, `np.dot` or `np.matmul` on whole matrices:

- `by_dots(A, B)`: entry $(i, j)$ is row $i$ of `A` dotted with column $j$ of `B` (`np.sum` of an elementwise product).
- `by_columns(A, B)`: column $j$ of the result is the combination of the columns of `A` with weights `B[:, j]`.
- `by_outer(A, B)`: the sum over $k$ of the outer product of column $k$ of `A` with row $k$ of `B` (`np.outer` is allowed).

Each raises `ValueError` if the inner sizes differ. The tests compare with `A @ B` and check an **invariant**: $(AB)C = A(BC)$ for random shapes.

## Hints

1. Loop over `i` and `j` and fill an array of zeros.
2. `sum(B[k, j] * A[:, k] for k in range(n))`.
3. Outer products give whole $m \times p$ matrices of rank one; add $n$ of them.
