# A scalar engine first

Before tensors, build the engine for single numbers. A `Value` holds `data`, a `grad` (starting at 0), its parents and a `_backward` closure.

Implement `__add__`, `__mul__`, `__pow__` (by a constant number), `tanh`, `exp` and `backward`. Plain numbers mixed with values must work on either side (`2 * v`, `v + 1`). `backward()` sets the output's gradient to 1, orders the graph topologically and calls each node's `_backward` in reverse order. Gradients accumulate with `+=`.

## Hints

1. Each operation returns `out = Value(result, (self, other))` and sets `out._backward` to a closure, for multiplication `self.grad += other.data * out.grad` and `other.grad += self.data * out.grad`.
2. `tanh`: the local derivative is `1 - t**2`, where `t` is the output.
3. A node used twice (as in `x * x`) must receive both contributions; that is why the closures add rather than assign.
