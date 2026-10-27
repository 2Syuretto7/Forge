# Cross-entropy two ways

Implement the mean softmax cross-entropy of `logits` (a Tensor of shape `(B, C)`) against integer labels `y`:

1. `cross_entropy(logits, y)`: built only from engine operations (subtract the row maximum as a constant, `exp`, `sum`, `log`, a one-hot mask, `mean`), so the engine derives its gradient automatically.
2. `cross_entropy_fused(logits, y)`: a single operation that computes the loss in NumPy and whose backward rule is the closed form from L05, $(P - Y_{\text{onehot}})/B$, times the incoming gradient.

The tests check that both agree in value and gradient, and that the fused version creates a single node.

## Hints

1. The row maximum must be wrapped as a new `Tensor` with no parents, so it is a constant to the engine; the loss does not depend on it mathematically.
2. Pick the correct-class logit with `(z * onehot).sum(axis=1, keepdims=True)` where `onehot = np.eye(C)[y]`.
3. For the fused version, compute the log-probabilities stably with log-sum-exp, and in the backward rule rebuild `P` from them.
