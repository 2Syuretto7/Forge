# The whole MLP: forward, backward, and a per-parameter gradient check

Assemble the layers into a network with any number of hidden layers. Parameters live in a dict: `W1, b1, W2, b2, ...`; the last layer is linear and feeds softmax cross-entropy.

- `init_mlp(sizes, seed)`: for `sizes = [n_in, h1, ..., n_out]`, He initialization $W_i \sim \mathcal N(0, 2/n_{\text{in}})$ drawn in order with `np.random.default_rng(seed)`, biases zero.
- `loss_and_grads(params, X, y, act)`: forward pass with activation `"relu"` or `"tanh"` on hidden layers, then backward. Return `(loss, grads)` with `grads` keyed like `params`.
- `predict(params, X, act)`: the argmax class.

The tests check every parameter of a three-layer network against central differences.

## Hints

1. Loop over layers in the forward pass, saving each layer's input and pre-activation.
2. Loop backward from the last layer; apply the activation's backward only for hidden layers.
3. `len(sizes) - 1` linear layers in total.
