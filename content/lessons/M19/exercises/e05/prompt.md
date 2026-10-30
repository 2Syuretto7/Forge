# Dual numbers

Implement forward-mode differentiation with dual numbers (Section 4).

- A class `Dual(val, eps)` supporting `+`, `-`, `*`, `/` with other duals and with plain numbers on either side, unary minus, `**` with a numeric exponent, and comparisons `<`, `>` (by value, so programs with `if` statements still work).
- Functions `exp`, `log`, `sin`, `cos`, `tanh`, `sqrt` that accept either a `Dual` or a plain float and return the same kind.
- `derivative(f, x)`: evaluate `f(Dual(x, 1.0))` and return the `eps` part as a float.

The tests differentiate several functions and compare with exact derivatives to $10^{-12}$: no step size, no truncation error.

## Hints

1. `__radd__ = __add__` and `__rmul__ = __mul__`; subtraction and division need their own reflected versions.
2. `x ** p` for a dual: value $a^p$, eps $p a^{p-1} b$.
3. A helper `_lift(v)` that turns numbers into `Dual(v, 0.0)` keeps the operators short.
