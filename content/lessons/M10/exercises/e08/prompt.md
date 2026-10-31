# Multiplying in blocks

- `block_matmul(A, B, bs)`: compute $AB$ by cutting both matrices into tiles of at most `bs` rows and columns: the $(I, J)$ tile of the result is $\sum_K A_{IK} B_{KJ}$, where each tile product may use `@`. Sizes need not be multiples of `bs`.
- `tile_count(m, n, p, bs)`: how many tile products the loop performs, $\lceil m/bs \rceil \cdot \lceil n/bs \rceil \cdot \lceil p/bs \rceil$.

GPUs multiply this way (L08): each tile fits in fast memory, and the result is the same up to rounding.

## Hints

1. `range(0, m, bs)` gives the starting row of every tile; slicing past the end is safe.
2. Accumulate into `C[i:i + bs, j:j + bs]`.
3. `-(-m // bs)` is the ceiling of `m / bs`.
