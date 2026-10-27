# Counting the FLOPs of training

Section 5 estimated that a training step costs about three forward passes. Count it exactly for an MLP with layer sizes `sizes` and batch size `B`, counting a multiply-add as 2 FLOPs and ignoring elementwise operations.

- `forward_flops(sizes, B)`: $\sum_i 2B\,n_{i}\,n_{i+1}$.
- `backward_flops(sizes, B)`: two products per layer, except that the first layer does not need the gradient with respect to the input data.
- `params(sizes)`: weights plus biases.
- `flops_per_param_per_example(sizes, B)`: total training FLOPs divided by `params * B`.

For wide layers the last ratio approaches 6, the rule behind $C \approx 6ND$.

## Hints

1. Backward per layer: $2B n_i n_{i+1}$ for $dW$ plus the same for $dX$.
2. Subtract the first layer's $dX$ product.
3. Biases add parameters but almost no FLOPs.
