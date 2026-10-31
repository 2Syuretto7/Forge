# Softmax cross-entropy as a layer

The last layer turns logits `Z` `(B, K)` and integer labels `y` into a scalar loss, averaged over the batch.

- `softmax_ce_forward(Z, y)` returns `(loss, cache)` computed stably.
- `softmax_ce_backward(cache)` returns `dZ = (P - onehot(y)) / B`.

## Hints

1. Subtract each row's max before exponentiating.
2. Cache the probabilities and the labels.
3. The gradient of each row sums to zero.
