# Break it: a plateau that is not the optimum

Train logistic regression (the starter's `X`, `y`, `loss` and `grad`) with constant-step SGD on single examples. The loss falls, then flattens, and it is tempting to stop: but the plateau is the noise floor, not the minimum.

- `sgd_constant(step, epochs, rng)`: SGD over shuffled single examples; return the full loss after each epoch.
- `sgd_decaying(step0, epochs, rng)`: the same, with step $\eta_0/(1 + t/n)$ after $t$ examples ($n$ the number of rows).
- `gap_to_optimum(losses)`: the last loss minus the starter's `F_STAR`, the minimum found by full-batch Newton iterations.

The tests show the constant step stalled well above the optimum and the decaying step much closer after the same number of epochs.

## Hints

1. A permutation per epoch: `rng.permutation(n)`.
2. A single-example gradient is `x * (sigmoid(x @ w) - y)`.
3. A plateau is diagnosed by halving the step: if the plateau drops, it was noise.
