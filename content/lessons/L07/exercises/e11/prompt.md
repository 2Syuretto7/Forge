# Break it: dead ReLUs

Measure how many ReLU units are dead, and show that dead units receive exactly zero gradient.

- `dead_fraction(W1, b1, X)`: the fraction of hidden units whose pre-activation $XW_1 + b_1$ is $\le 0$ for **every** row of `X`.
- `first_layer_grads(params, X, y)`: the gradients of `W1` and `b1` for a `2 -> h -> 3` ReLU network (copy your `loss_and_grads`); return `(dW1, db1)`.

The tests kill most units with a large negative bias and check that their gradient columns are exactly zero.

## Hints

1. `active = (X @ W1 + b1) > 0`; a unit is dead if `active[:, j]` is all false.
2. Dead columns of `dW1` and entries of `db1` must be exactly `0.0`, not merely small.
3. A large negative bias is the easiest way to kill a unit; a destructive learning-rate step does the same in practice.
