# The z-loss

The softmax is unchanged when a constant is added to every logit, so nothing stops the logits from drifting to huge values, where low-precision arithmetic breaks down. PaLM added a small penalty on $\log Z = \operatorname{logsumexp}(z)$, the **z-loss** $10^{-4} (\log Z)^2$, which keeps $\log Z$ near zero.

Implement `ce_with_z_loss(logits, y, z_coef)`: the mean cross-entropy plus `z_coef` times the mean of $(\log Z)^2$, and the gradient with respect to the logits.

## Hints

1. Compute $\log Z$ stably: subtract the row maximum before exponentiating.
2. The cross-entropy gradient is $(p - \text{onehot}(y))/n$; the z-loss adds $2\,c\,\log Z \cdot p / n$, since $\partial \log Z/\partial z = p$.
3. With $c = 0$ the result must be plain cross-entropy.
