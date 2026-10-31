# Activation layers

Implement ReLU and tanh as layers with a forward pass that returns a cache and a backward pass that maps the output gradient to the input gradient.

- `relu_forward(Z)` returns `(Y, cache)`; `relu_backward(dY, cache)` returns `dZ`, using the convention that the derivative at exactly 0 is 0.
- `tanh_forward(Z)` returns `(Y, cache)`; `tanh_backward(dY, cache)` returns `dZ`, computed from the saved output.

## Hints

1. ReLU mask: `Z > 0`.
2. For tanh, cache the output `Y` and use $1 - Y^2$.
3. The ReLU gradient check avoids inputs within $10^{-3}$ of zero, where the derivative jumps.
