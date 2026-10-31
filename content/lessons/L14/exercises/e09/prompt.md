# Activation checkpointing

Backpropagation needs every layer's activations, so memory grows with depth. Checkpointing keeps only some of them and recomputes the rest during backward.

The network is $h_{i+1} = \tanh(h_i W_i)$.

1. `forward(x, Ws)`: all activations $h_0, \dots, h_L$.
2. `backward(hs, Ws, dout)`: the gradients of every $W_i$ given $\partial L/\partial h_L$.
3. `checkpointed_grads(x, Ws, dout, k)`: keep only $h_0, h_k, h_{2k}, \dots$ in the forward pass; in backward, for each segment from last to first, recompute its activations from its checkpoint and backpropagate through it. Return the gradients and the peak number of stored activations (checkpoints plus one recomputed segment).

## Hints

1. With $z = h_i W_i$ and $h_{i+1} = \tanh z$: $\partial z = \partial h_{i+1} \odot (1 - h_{i+1}^2)$, $\partial W_i = h_i^\top \partial z$, $\partial h_i = \partial z\, W_i^\top$.
2. Memory is about $L/k + k$ activations, smallest at $k \approx \sqrt{L}$; the price is one extra forward pass.
3. The gradients must be identical to the uncheckpointed ones: recomputation is exact.
