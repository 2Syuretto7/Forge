# Variance-preserving initialization

A layer $y = Wx$ with $n_{\text{in}}$ inputs and weights of variance $v$ gives each output variance $n_{\text{in}}\,v\,\mathbb{E}x_j^2$ (Section 5). After a ReLU, $\mathbb{E}\,\mathrm{relu}(z)^2 = \frac12\operatorname{Var}z$ for symmetric $z$, so the second moment of the activations is multiplied by $\frac12n_{\text{in}}v$ per layer. **He initialization**, $v = 2/n_{\text{in}}$, makes the factor exactly 1; Xavier's $v = 1/n_{\text{in}}$ suits layers without the ReLU's halving.

- `relu_gain(n_in, v)`: $\frac12n_{\text{in}}v$.
- `he_variance(n_in)` and `xavier_variance(n_in)`.
- `layer_second_moments(x, W)`: `(E x^2, E y^2, E relu(y)^2)` averaged over all entries, for a batch `x` of shape `(batch, n_in)` and `W` of shape `(n_in, n_out)`.

The tests draw a layer of width 512 and check every factor against the derivation.

## Hints

1. Half of a symmetric variable's mass is below zero, where the ReLU outputs 0; the other half keeps its square.
2. `np.maximum(y, 0)`.
3. The backward pass multiplies gradient variances by $\frac12n_{\text{out}}v$; the two conditions differ only when the widths do.
