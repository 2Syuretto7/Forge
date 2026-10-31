# Classification metrics

For predicted probabilities `P` `(n, K)` and integer labels `y`:

- `accuracy(P, y)`.
- `log_loss(P, y)`: mean $-\log P_{i, y_i}$, with probabilities clipped to $[10^{-15}, 1]$ so a single zero cannot make it infinite.
- `confusion_matrix(P, y, K)`: `C[true, predicted]` counts.

## Hints

1. Predicted class: `P.argmax(axis=1)`.
2. `np.add.at(C, (y, pred), 1)` fills the confusion matrix.
3. The diagonal of the confusion matrix sums to the number of correct predictions.
