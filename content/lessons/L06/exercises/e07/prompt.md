# Statistics through depth

Implement `layer_stats(p, X, y, depth, mode)`: return two lists of length `depth`, the root mean square of the hidden state after each layer, and the root mean square of the gradient of each `W{l}` (from your `stack_loss_and_grads`, provided).

Then compare the five variants at depth 20 and width 64 on 200 digits, at initialization. Which variants keep the activations at a stable scale? Which keep the gradients similar across layers?

## Hints

1. Recompute the forward pass layer by layer, recording `sqrt(mean(h**2))` after each update.
2. For the gradients, call `stack_loss_and_grads` once and read `grads[f"W{l}"]`.
3. The last layer's gradient is the one closest to the loss; compare the first with the last.
