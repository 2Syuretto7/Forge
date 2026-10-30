# The cost of brute force

Size a brute-force search engine before you build it (M01's habit).

- `index_bytes(n, d, bytes_per=4)`: memory for `n` vectors of length `d`.
- `query_seconds(n, d, flops_per_s)`: the time of one query at a sustained rate, $2nd$ FLOPs.
- `max_vectors(memory_bytes, d, bytes_per=4)`: how many vectors fit.
- `queries_per_second(n, d, flops_per_s)`: the reciprocal of `query_seconds`.

The tests size an index of a billion 768-dimensional embeddings.

## Hints

1. `n * d * bytes_per`.
2. `2 * n * d / flops_per_s`.
3. Integer division for `max_vectors`.
