# Train on the spiral and compare with L07

The full engine is provided. `make_spiral()` returns 300 points of three interleaved spiral arms (a classic dataset no linear classifier can separate), and `manual_grads(model, X, y)` is the hand-written backward pass from L07 for the same network.

Implement `train(sizes, X, y, lr, steps, seed=0)`: build `MLP(sizes, seed)`, an `SGD` optimizer, and run `steps` full-batch steps of zero-grad, forward, `cross_entropy_fused`, backward, step. Return `(model, losses)` with the loss of every step as a float.

The tests check that your engine's gradients equal L07's hand-written ones to machine precision, and that a `2-64-3` network trained for 300 steps at learning rate 1 classifies the spiral with at least 90 percent training accuracy.

## Hints

1. Call `opt.zero_grad()` before `loss.backward()`; without it, gradients from all earlier steps accumulate.
2. Wrap the input once per step: `model(Tensor(X))`.
3. Record `float(loss.data)` after the backward pass.
