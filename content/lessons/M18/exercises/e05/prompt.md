# The chain rule through a network

A small network: $h_1 = \tanh(W_1 x)$, $h_2 = \tanh(W_2 h_1)$, $y = W_3 h_2$.

- `forward(Ws, x)`: return the list `[x, h1, h2, y]`.
- `layer_jacobians(Ws, x)`: the Jacobians of the three stages at the points the forward pass visits: $\operatorname{diag}(1 - h_1^2) W_1$, $\operatorname{diag}(1 - h_2^2) W_2$ and $W_3$.
- `network_jacobian(Ws, x)`: their product in the right order, the Jacobian of $y$ with respect to $x$.

The tests run a **gradient check** against a numerical Jacobian of the whole network.

## Hints

1. The derivative of $\tanh$ is $1 - \tanh^2$, available from the stored activations.
2. The last stage applies last, so its Jacobian stands leftmost.
3. Shapes: $(m \times k_2)(k_2 \times k_1)(k_1 \times n)$.
