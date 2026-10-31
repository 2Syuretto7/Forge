# Unbroadcasting a gradient

Implement `unbroadcast(g, shape)`: given the gradient `g` of a broadcast result, return the gradient of the input that had shape `shape`, by summing over every axis that broadcasting added or stretched. The result must have exactly shape `shape`.

Examples: `g` of shape `(32, 4)` and `shape=(4,)` gives the column sums; `shape=(32, 1)` gives the row sums kept as a column; `shape=()` gives the sum of everything.

## Hints

1. While `g` has more dimensions than `shape`, sum over axis 0.
2. Then, for each axis where `shape` has size 1 but `g` does not, sum over it with `keepdims=True`.
3. Check your function against NumPy: for `x` of shape `shape`, the gradient of `np.sum(G * (Z + x))` with respect to `x` is `unbroadcast(G, shape)`.
