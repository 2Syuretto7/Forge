# The missing transpose

A linear layer has weights `W` of shape `(d_out, d_in)` and bias `b` of shape `(d_out,)`.

- `linear(x, W, b)`: the outputs for a batch `x` of shape `(N, d_in)`: $x W^\top + b$, shape `(N, d_out)`.
- `wrong_runs(d_in, d_out)`: whether the buggy `x @ W + b` runs without an error for these sizes (it needs `d_in == d_out`, since `x @ W` needs `d_in` rows in `W` and the result's `d_in` columns must broadcast with `b`).
- `detect_transpose_bug(f, d=4, seed=0)`: given a function `f(x, W, b)` claiming to be a linear layer, return `True` if it disagrees with `linear` on random square inputs.

## Hints

1. `x @ W.T + b`.
2. Work out the shapes: `(N, d_in) @ (d_out, d_in)` needs `d_in == d_out`.
3. Square layers hide the bug from shape checks but not from a numerical comparison.
