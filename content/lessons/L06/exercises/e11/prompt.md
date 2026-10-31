# Break it: batch norm with a batch of one

Your batch norm and layer norm, forward and backward, are provided.

1. `batch_of_one(x, gamma, beta)`: run training-mode batch norm on a batch containing only the row `x`, and its backward pass with an upstream gradient of ones. Return `(y, dx)` for that row.
2. `layernorm_of_one(x, gamma, beta)`: the same row through layer norm, with an upstream gradient that weights the features $1, 2, \dots, d$. Return `(y, dx)`.

Batch norm returns $\beta$ and a zero gradient whatever `x` is; layer norm still works.

## Hints

1. `x[None, :]` turns the vector into a batch of one.
2. Return the first (only) row of each result.
3. An upstream gradient of ones would give layer norm a zero gradient too, for a different reason (it is a constant shift of the row), which is why the test weights the features.
