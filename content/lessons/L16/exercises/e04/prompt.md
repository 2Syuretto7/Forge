# Merging and counting

1. `merge(W0, A, B, alpha)`: the single matrix $W_0 + \frac{\alpha}{r} B A$ that behaves exactly like the LoRA layer; merged, the adapter costs nothing at inference.
2. `lora_params(d_in, d_out, r)`: the trainable parameters of a rank-$r$ adapter, $r(d_\text{in} + d_\text{out})$.
3. `trainable_fraction(n_layer, d, r, per_layer=("q", "v"))`: the fraction of a transformer's $12\,n_\text{layer} d^2$ block parameters trained by rank-$r$ adapters on the listed $d \times d$ projections of every layer.

## Hints

1. Merging is exact: $x W^\top = x W_0^\top + \frac{\alpha}{r} x A^\top B^\top$.
2. Several adapters can share one base model and be swapped per request, unmerged.
3. The fraction does not depend on the number of layers.
