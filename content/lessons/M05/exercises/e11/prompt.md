# The cost of naive matrix multiplication

- `matmul(A, B)`: multiply two square matrices given as lists of rows, with three nested loops, returning `(C, multiply_adds)` where the count is the number of times the innermost `C[i][j] += A[i][k] * B[k][j]` runs.
- `predicted_multiply_adds(n)`: the closed form.
- `predicted_ratio(n)`: the predicted cost ratio of size $2n$ to size $n$.

The tests check your product against NumPy, the count against the formula, and that the ratio of counts at sizes 16 and 32 matches the prediction.

## Hints

1. Start `C` as `[[0.0] * n for _ in range(n)]`.
2. The innermost body runs once for each triple `(i, j, k)`.
3. $(2n)^3 / n^3$.
