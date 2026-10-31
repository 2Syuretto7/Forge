# Matrix multiplication, transpose and reshape

Add three structural operations to the engine (the previous stage is provided):

- `_matmul(self, other)` for `self @ other` with 2-D operands: the gradient is `G @ B.T` to `A` and `A.T @ G` to `B`.
- `_transpose(self)`, used as the property `t.T`: the gradient is `G.T`.
- `_reshape(self, *shape)`: the gradient is `G` reshaped to the input's shape.

They are attached to the class at the bottom of the file.

## Hints

1. Follow the pattern of `__add__`: compute, create the output with its parents and an op name, attach a closure, return.
2. Shapes check the matmul rule: `G` is `(m, n)`, `B` is `(k, n)`, so `G @ B.T` is `(m, k)`, the shape of `A`.
3. Do not unbroadcast in matmul here; the operands are 2-D and not broadcast.
