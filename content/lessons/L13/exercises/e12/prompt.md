# Break it: a mask that leaks the future

Your softmax is provided.

1. `leaks_future(attn_fn, X, eps=1e-3)`: `attn_fn` maps an `(n, d)` sequence to an `(n, d)` output. For each position $t \ge 1$, add `eps` to row $t$ of a copy of `X` and check whether any output row before $t$ changes by more than `1e-12`. Return `True` as soon as one does.
2. `off_by_one_mask(n)`: the bug, a mask that hides key $j$ from query $i$ only when $j > i + 1$.

The tests build attention with the correct mask and with yours, and check that only the buggy one leaks.

## Hints

1. Compute the unperturbed output once.
2. Compare `out[:t]` only: changes at $t$ and later are allowed.
3. `np.triu(..., k=2)` leaves the first superdiagonal unmasked.
