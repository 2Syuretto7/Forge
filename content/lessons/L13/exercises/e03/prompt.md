# The backward pass of attention

Your softmax, its backward pass and `attention` are provided. Implement `attention_backward(dO, Q, K, V, P, scale=True)` returning $(\text{d}Q, \text{d}K, \text{d}V)$, using the formulas from the derivation. It must be correct with and without the causal mask: masked weights are exactly 0, and the softmax backward pass then sends them no gradient.

## Hints

1. $\text{d}V = P^\top \text{d}O$ and $\text{d}P = \text{d}O\, V^\top$.
2. $\text{d}S$ is `softmax_backward(P, dP)` times the scale $c$.
3. $\text{d}Q = \text{d}S\, K$ and $\text{d}K = \text{d}S^\top Q$.
