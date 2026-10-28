# A fused cross-entropy

Implement `fused_cross_entropy(logits, y, block=8)`: for each row of `logits` (shape `(B, V)`), compute its log-sum-exp in one pass over vocabulary blocks with a running maximum and sum, as in exercise 1; the loss is the mean over rows of $\text{lse} - \text{logit}_{y}$. Then write the gradient $(\operatorname{softmax} - \text{onehot}(y))/B$ once, from the log-sum-exp, without storing a separate probability array. Return `(loss, dlogits)`.

## Hints

1. The softmax is `exp(logits - lse[:, None])`.
2. Subtract 1 at each row's target before dividing by `B`.
3. Check against L05's cross-entropy gradient.
