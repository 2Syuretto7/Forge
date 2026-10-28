# Attribution patching

Patching every component of a large model one by one takes one forward pass each. A first-order estimate needs a single backward pass: the effect of moving component $i$ from corrupted to clean is about $(a_\text{clean} - a_\text{corrupt})_i \cdot \partial m / \partial a_i$, evaluated at the corrupted run.

1. `metric_and_grad(a, W, v)`: $m = v \cdot \tanh(W a)$ and $\partial m / \partial a$.
2. `attribution_patching(a_clean, a_corrupt, W, v)`: all the first-order estimates at once.
3. `exact_patching(a_clean, a_corrupt, W, v)`: the exact effect of patching each component alone.

## Hints

1. $\partial m/\partial a = W^\top (v \odot (1 - h^2))$ with $h = \tanh(Wa)$.
2. The estimate is accurate when the clean and corrupted activations are close, and degrades when they differ a lot.
3. Use the estimate to rank candidates, then confirm the top ones with exact patching.
