# A 30-layer stack in five variants

The L03 digits and your layer norm are provided, with `init_stack(depth, width, ...)`, which creates `Win`, per-layer `W{l}`, `g{l}`, `b{l}`, a final `gf`, `bf` and `Wout`. With $F(u) = \operatorname{relu}(u W_l)$ and LN the layer norm with $g_l, b_l$, the variants are:

| mode | layer |
| --- | --- |
| `plain` | $h \leftarrow F(h)$ |
| `plain_ln` | $h \leftarrow F(\operatorname{LN}(h))$ |
| `res` | $h \leftarrow h + F(h)$ |
| `pre` | $h \leftarrow h + F(\operatorname{LN}(h))$, and a final LN with `gf`, `bf` before `Wout` |
| `post` | $h \leftarrow \operatorname{LN}(h + F(h))$ |

The input is `h = X @ Win` and the logits are `h @ Wout`.

1. `stack_forward(p, X, depth, mode)` returns `(logits, hidden, caches)`, where `hidden` is what multiplies `Wout`.
2. `stack_loss_and_grads(p, X, y, depth, mode)` returns the mean softmax cross-entropy and a gradient for **every** key of `p` (zeros for parameters a variant does not use).

## Hints

1. Cache, per layer, the input to the matrix product `u`, the pre-activation `z`, and the layer-norm cache.
2. In the backward pass, a residual variant adds the branch's input gradient to the stream's: `dh = dh + du`. Post-norm goes through the norm first.
3. Gradient-check each variant on a 3-layer, width-8 stack before trusting it at depth 30.
