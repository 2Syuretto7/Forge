# Three norms

For NumPy arrays:

- `l1(x)`, `l2(x)`, `linf(x)`: the three norms of Section 6.
- `in_unit_ball(x, p)`: whether $\|x\|_p \leq 1$ for `p` one of `1`, `2` or `"inf"`.
- `clip_by_norm(x, max_norm)`: if $\|x\|_2 >$ `max_norm`, scale `x` down so its length is exactly `max_norm`; otherwise return it unchanged. This is gradient clipping (L19).

The tests check an **invariant**: for random vectors in $d$ dimensions, $\|x\|_\infty \leq \|x\|_2 \leq \|x\|_1 \leq \sqrt{d}\,\|x\|_2$, and each norm satisfies the triangle inequality.

## Hints

1. `np.sum(np.abs(x))`, `np.sqrt(np.sum(x * x))`, `np.max(np.abs(x))`.
2. A dictionary from `p` to the norm function.
3. Multiply by `max_norm / l2(x)` when clipping.
