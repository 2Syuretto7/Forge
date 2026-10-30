# Shapes and costs of products

Work out shapes before computing anything.

- `matmul_shape(s1, s2)`: the shape of `A @ B` for shapes `s1` and `s2` (tuples), following NumPy: two 2-D shapes `(m, n)` and `(n, p)` give `(m, p)`; a 1-D second shape `(n,)` gives `(m,)`; 3-D shapes `(b, m, n)` and `(b, n, p)` give `(b, m, p)`, and a batch size of 1 on one side stretches to the other's. Raise `ValueError` when the inner sizes differ or the batch sizes clash.
- `matmul_flops(s1, s2)`: $2mnp$ times the batch size (with $p = 1$ for a vector).

## Hints

1. Handle the vector case first: treat `(n,)` as `(n, 1)` and drop the last axis at the end.
2. Pad 2-D shapes to 3-D with a batch of 1.
3. Batch sizes `b1` and `b2` are compatible when equal or when one is 1.
