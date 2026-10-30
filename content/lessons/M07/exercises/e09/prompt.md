# A rotary position encoding

For a vector $x$ of even length $d$, the rotary encoding at position $m$ turns each pair $(x_{2j}, x_{2j+1})$ by the angle $m\,\omega_j$, where $\omega_j = \text{base}^{-2j/d}$: the first pair turns fastest and later pairs ever more slowly.

- `frequencies(d, base=10000)`: the list of the $d/2$ speeds $\omega_j$.
- `rope(x, m, base=10000)`: the encoded vector, as a list (use the rotation formula on each pair).
- `dot(u, v)`: the dot product $\sum u_i v_i$.
- `score(q, k, m, n)`: the dot product of the query encoded at position `m` and the key encoded at position `n`.

The tests check that the encoding preserves length, and that `score(q, k, m, n)` equals `score(q, k, m + s, n + s)` for any shift `s`: the score sees only the distance between positions.

## Hints

1. `[base ** (-2 * j / d) for j in range(d // 2)]`.
2. For pair `j`, rotate `(x[2j], x[2j + 1])` by `m * omega[j]`.
3. The capstone proves why the shift property holds.
