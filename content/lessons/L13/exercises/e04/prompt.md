# Multi-head attention

1. `split_heads(X, h)`: reshape `(n, d)` into `(h, n, d // h)`, head `i` taking columns `i * d/h` to `(i + 1) * d/h`.
2. `merge_heads(Y)`: the inverse.
3. `mha_forward(X, Wq, Wk, Wv, Wo, h, causal=True)`: project to $Q, K, V$, split into heads, run your single-head `attention` (provided) in each, merge, and project with $W_O$. Return `(Y, cache)` with `cache = (X, Q, K, V, P, M)`: the split $Q, K, V$, the stacked weights `P` of shape `(h, n, n)`, and the merged head outputs `M`.

## Hints

1. `X.reshape(n, h, d // h).transpose(1, 0, 2)`.
2. A loop over the `h` heads is fine; exercise 5 differentiates it.
3. With `h = 1`, the result equals plain attention followed by $W_O$.
