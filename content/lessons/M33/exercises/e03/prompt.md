# Blocked matrix multiplication

Model the memory hierarchy as a small fast cache in front of a large slow memory, and count the words that cross between them (Section 2). The naive triple loop computes each output $C_{ij}$ by reading a row of $A$ and a column of $B$ from slow memory: $2n$ words per output. The blocked algorithm splits the matrices into $b \times b$ tiles; for each output tile it streams $n/b$ pairs of tiles through the cache, so each word it reads is used $b$ times.

- `blocked_matmul(A, B, b)`: the product, computed tile by tile with NumPy products of sub-blocks; the tile size need not divide the dimensions.
- `traffic_naive(n)`: $2n^3 + n^2$ words for square matrices, counting the writes of $C$.
- `traffic_blocked(n, b)`: $2n^3/b + n^2$ words.
- `best_tile(cache_words)`: the largest $b$ with three tiles in cache, $3b^2 \le$ `cache_words`.

The tests check the product, the factor of $b$ between the two traffic counts, and the tile for a cache of 8,192 words (32 KB of fp32).

## Hints

1. Loop over tile indices `i0, j0, p0` in steps of `b`; slicing past the end of an array simply stops at the end.
2. Accumulate `C[i0:i0+b, j0:j0+b] += A[i0:i0+b, p0:p0+b] @ B[p0:p0+b, j0:j0+b]`.
3. `int(math.isqrt(cache_words // 3))` is a good start; check the boundary.
