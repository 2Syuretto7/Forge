# Elementwise operations

Add the elementwise operations a network needs (earlier stages provided). A helper `_unary(self, value, local, op)` is given: it creates the output and a backward rule that multiplies the incoming gradient by `local()`.

Implement `_exp`, `_log`, `_relu`, `_tanh`, `_pow` (by a constant), and the derived operations `_neg`, `_sub`, `_rsub`, `_div`, `_rdiv` and `_mean(axis=None, keepdims=False)`. The derived ones need no backward rule of their own: build them from operations that already have one.

## Hints

1. `exp`: the local derivative is the output itself; `log`: `1 / x`; `relu`: `(x > 0)`; `tanh`: `1 - t**2`; `pow`: `p * x**(p-1)`.
2. `a - b` is `a + (-b)`; `a / b` is `a * b**-1`; `mean` is a `sum` times `1/n`.
3. `_rsub` and `_rdiv` handle a number on the left, as in `1 - t` and `1 / t`.
