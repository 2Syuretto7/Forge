# The softmax and its backward pass

1. `softmax_rows(S)`: the softmax of every row (last axis) of `S`, computed stably by subtracting the row maximum. Entries equal to `-inf` must get weight exactly 0.
2. `softmax_backward(P, dP)`: given the softmax output `P` and $\partial L/\partial P$, return $\partial L/\partial S$, row by row.

Both must work for arrays with any number of leading dimensions (for example `(heads, n, n)`).

## Hints

1. `np.exp(-np.inf)` is `0.0`, so masked entries need no special case once the maximum is subtracted.
2. For one row, $\partial L/\partial s = p \odot (g - p^\top g)$ with $g = \partial L/\partial p$.
3. Use `axis=-1, keepdims=True` throughout.
