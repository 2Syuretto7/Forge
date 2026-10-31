# Gumbel-max and Gumbel-softmax

A categorical sample can be written as a deterministic function of the logits and fixed noise: with independent Gumbel variables $g_i = -\log(-\log u_i)$, $u_i$ uniform, the index $\arg\max_i(z_i + g_i)$ has exactly the distribution $\mathrm{softmax}(z)$, the **Gumbel-max trick** (Section 4). The argmax is not differentiable; replacing it by a softmax at temperature $\tau$ gives the **Gumbel-softmax** relaxation $y = \mathrm{softmax}((z + g)/\tau)$, a point in the simplex that approaches a one-hot vector as $\tau \to 0$.

- `gumbel(shape, rng)`.
- `gumbel_max(z, n, rng)`: $n$ sampled indices.
- `gumbel_softmax(z, tau, n, rng)`: an $n \times K$ array of relaxed samples.
- `mean_max_entry(Y)`: the average over rows of the largest entry, a measure of how close the samples are to one-hot.

The tests check the Gumbel-max frequencies against the softmax, and that the relaxed samples are near one-hot at $\tau = 0.1$ and near uniform at $\tau = 10$.

## Hints

1. Add the noise to the logits row by row: `z + gumbel((n, K), rng)`.
2. Use a stable softmax along axis 1.
3. Low temperatures make the relaxation accurate and its gradients noisy; high temperatures the reverse. The trade-off is set by $\tau$.
