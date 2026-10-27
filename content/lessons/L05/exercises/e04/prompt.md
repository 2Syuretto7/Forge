# The logistic loss and its gradient

Implement Section 3 for labels $y \in \{0, 1\}$, weights `w` `(d,)` and bias `b`.

- `sigmoid(a)`: stable for large $|a|$ (no overflow warnings).
- `logistic_loss(w, b, X, y)`: mean binary cross-entropy computed from logits with the stable formula of L04.
- `logistic_grad(w, b, X, y)`: returns `(dw, db)` $= \big(\tfrac1n X^\top(\sigma(a) - y),\ \text{mean}(\sigma(a) - y)\big)$.

## Hints

1. Stable sigmoid: use `np.where(a >= 0, 1 / (1 + exp(-a)), exp(a) / (1 + exp(a)))`, computing each branch on a clipped or masked argument.
2. Loss: `np.mean(np.maximum(a, 0) - a * y + np.log1p(np.exp(-np.abs(a))))`.
3. The gradient is "features times prediction error".
