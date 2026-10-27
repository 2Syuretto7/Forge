# Forward mode versus reverse mode, counted

Build a full Jacobian both ways and count the passes (Section 4). You receive two black boxes for a function $f: \mathbb{R}^n \to \mathbb{R}^m$:

- `jvp(v)` returns $Jv$ for a vector `v` of length $n$;
- `vjp(u)` returns $u^\top J$ for a vector `u` of length $m$.

Implement:

- `jacobian_forward(jvp, n)`: build $J$ column by column from JVPs with unit vectors. Return `(J, passes)`.
- `jacobian_reverse(vjp, m)`: build $J$ row by row from VJPs. Return `(J, passes)`.
- `cheaper_mode(n, m)`: `"forward"` if $n < m$, `"reverse"` if $m < n$, `"either"` if equal.

## Hints

1. `np.eye(n)[j]` is the $j$-th unit vector.
2. Stack columns with `np.stack(cols, axis=1)` and rows with `np.stack(rows, axis=0)`.
3. The pass count is just the number of calls you made.
