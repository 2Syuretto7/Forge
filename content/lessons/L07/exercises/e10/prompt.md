# Break it: symmetric initialization

Train a `2 -> 8 -> 3` tanh network on the spiral twice: once from random weights, once with every hidden unit given **identical** incoming and outgoing weights (all entries of `W1` equal to 0.1, all entries of `W2` equal to 0.1, biases zero).

- `symmetric_init(sizes, value)`: weights filled with `value`, biases zero.
- `unit_spread(W1)`: how different the hidden units are, measured as the largest distance between any two columns of `W1`.
- `train_full_batch(params, X, y, lr, steps)`: plain gradient descent on the full data (copy your `loss_and_grads` with tanh). Return the final loss.

The tests show that the symmetric network's hidden units stay exactly identical however long it trains, and that its loss stays far above the randomly initialized network's.

## Hints

1. `np.full((a, b), value)`.
2. Column distance: compare every pair of columns of `W1`, or use `np.max(W1, axis=1) - np.min(W1, axis=1)`.
3. Use tanh for both runs: with ReLU and these weights the effect is the same, but tanh keeps every gradient nonzero, which makes the point sharper.
