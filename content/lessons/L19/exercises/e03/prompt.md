# Attention logits and QK-layernorm

When queries and keys grow during training, attention logits $q \cdot k / \sqrt{d}$ grow with them, the softmax collapses onto one key, and training stalls or diverges. Normalizing $q$ and $k$ with a layer norm before the product bounds the logits.

1. `layer_norm(x, eps=1e-5)` over the last axis (no gain or bias), returning $y$ and a cache.
2. `layer_norm_backward(dy, cache)`: the gradient with respect to $x$.
3. `max_attention_logit(q, k, qk_norm)`: the largest $|q_i \cdot k_j|/\sqrt{d}$, with the rows of $q$ and $k$ layer-normalized first when `qk_norm`.

## Hints

1. With $\hat x = (x - \mu)\,r$, $r = 1/\sqrt{\sigma^2 + \epsilon}$: $\partial x = r\,(\partial \hat x - \overline{\partial \hat x} - \hat x\, \overline{\partial \hat x \odot \hat x})$, the means taken over the last axis.
2. A normalized row has norm about $\sqrt{d}$, so by Cauchy-Schwarz $|q \cdot k|/\sqrt d \le \sqrt d$.
3. With a learned gain the bound scales with the gain, which grows far more slowly than raw activations.
