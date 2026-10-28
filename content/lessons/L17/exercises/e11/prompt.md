# Break it: attention scores in fp16

1. `scores(Q, K, dtype)`: $QK^\top$ with inputs and result in `dtype`, as an fp16 matrix product without scaling computes it.
2. `scaled_first(Q, K, dtype)`: divide $Q$ by $\sqrt d$ before the product.
3. `stable_lse(x)`: $\log \sum_j e^{x_j}$ of a vector, computed in float64 after subtracting the maximum, and its gradient, the softmax.

With large activations, the fp16 scores overflow to infinity; scaling first keeps them finite, and the softmax that follows must still be computed stably.

## Hints

1. `Q.astype(dtype) @ K.astype(dtype).T`.
2. Scaling $Q$ by $1/\sqrt d$ is what attention does anyway; doing it before the product protects the range.
3. The gradient of the log-sum-exp is $e^{x - \text{lse}}$.
