# Broadcasting, checked

- `broadcast_shape(s1, s2)`: the shape NumPy produces for an elementwise operation on arrays of shapes `s1` and `s2`: line the shapes up from the right, pad the shorter with 1s on the left, and on each axis the sizes must be equal or one of them 1 (which stretches). Raise `ValueError` otherwise. Do not call NumPy's broadcasting helpers.
- `strict_sub(a, b)`: `a - b`, but raise `ValueError` if the shapes are not identical.
- `mse(pred, target)`: mean squared error that refuses mismatched shapes (use `strict_sub`).

## Hints

1. Pad with `(1,) * (n - len(s))`.
2. `zip` the padded shapes; where one size is 1, the result takes the other (even if it is 0).
3. The tests feed `mse` a `(100,)` prediction and a `(100, 1)` target.
