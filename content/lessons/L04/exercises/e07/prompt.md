# Stable cross-entropy from logits, batched

The workhorse loss of deep learning. For logits `Z` of shape `(B, K)` and integer targets `y` of shape `(B,)`:

- `logsumexp(Z)`: row-wise $\operatorname{LSE}$, shape `(B,)`, stable for huge or very negative logits.
- `cross_entropy(Z, y)`: the mean over the batch of $\operatorname{LSE}(z_b) - z_{b, y_b}$.
- `cross_entropy_grad(Z, y)`: the gradient of the mean loss with respect to `Z`, $(\operatorname{softmax}(Z) - \text{onehot}(y))/B$.

The tests include logits of size $\pm 1000$, where a naive implementation produces `nan`.

## Hints

1. `m = Z.max(axis=1, keepdims=True)`, then `m[:, 0] + log(sum(exp(Z - m), axis=1))`.
2. Pick the target logits with `Z[np.arange(B), y]`.
3. Softmax from LSE: `np.exp(Z - lse[:, None])`.
