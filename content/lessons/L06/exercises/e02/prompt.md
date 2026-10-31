# Running statistics for evaluation

Complete `BatchNorm.forward(x)`. In training mode (`self.training = True`) normalize with the batch statistics, as in exercise 1, and update the running averages with momentum $m$:

$$
\text{running\_mean} \leftarrow (1 - m)\,\text{running\_mean} + m\,\mu_B, \qquad \text{running\_var} \leftarrow (1 - m)\,\text{running\_var} + m\,\sigma^2_B \tfrac{N}{N - 1}.
$$

In evaluation mode, normalize with the running statistics and do not update them. This matches PyTorch's `BatchNorm1d`, which normalizes with the biased batch variance but stores the unbiased one.

## Hints

1. `x.var(axis=0)` is the biased variance; multiply by `n / (n - 1)` for the running estimate.
2. Compute `mu, var` in each branch, then share the final line `gamma * (x - mu) / sqrt(var + eps) + beta`.
3. In evaluation mode each example's output depends only on itself.
