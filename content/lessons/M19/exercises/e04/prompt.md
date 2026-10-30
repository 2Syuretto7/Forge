# Cross-entropy through the softmax

For logits `z` (a 1-D array) and a correct class `c`:

- `cross_entropy(z, c)`: $L = -\log p_c$ with $p = \operatorname{softmax}(z)$, computed stably as $\log\sum_j e^{z_j} - z_c$ (subtract the maximum first).
- `cross_entropy_grad(z, c)`: $\partial L / \partial z = p - y$, with $y$ the one-hot vector of class `c`.
- `chain_check(z, c)`: the same gradient assembled from the two VJPs of Section 6, the log VJP ($\bar p = -y / p$) followed by the softmax VJP ($\bar z = p \odot (\bar p - \bar p \cdot p)$); it must equal `cross_entropy_grad`.

The tests run a **gradient check** against central differences, including logits in the thousands, where the naive formula overflows.

## Hints

1. `m = z.max(); m + np.log(np.sum(np.exp(z - m))) - z[c]`.
2. `y = np.zeros_like(z); y[c] = 1`.
3. $\bar p \cdot p = -1$ here, so the chain simplifies to $p - y$.
