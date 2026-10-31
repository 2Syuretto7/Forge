# Memory traffic of products in attention

L09's attention computes scores $QK^\top$ for every pair of positions. Before writing it, size it.

- `scores_bytes(batch, heads, T, bytes_per=2)`: the bytes of the score tensor of shape `(batch, heads, T, T)`.
- `matmul_bytes(m, n, p, bytes_per=2)`: bytes read and written by one product of `(m, n)` and `(n, p)` if each matrix moves once: $(mn + np + mp)$ times `bytes_per`.
- `intensity(m, n, p, bytes_per=2)`: operations per byte, $2mnp$ divided by `matmul_bytes`.

High intensity means the product is limited by arithmetic, low intensity by memory; L07's roofline turns this into time.

## Hints

1. Plain arithmetic on integers.
2. For square matrices, intensity grows like $n / (3 \cdot \text{bytes\_per})$.
3. A matrix-vector product, $p = 1$, has intensity about 1 in half precision: memory bound.
