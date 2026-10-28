# The sparse autoencoder objective

A sparse autoencoder rewrites activations $x$ as a sparse combination of many learned directions:
$$
z = \operatorname{ReLU}\bigl((x - b_d) W_e^\top + b_e\bigr), \qquad \hat x = z W_d + b_d, \qquad \mathcal{L} = \|x - \hat x\|^2 + \lambda \textstyle\sum_j z_j,
$$
averaged over rows, with $m$ latents, usually many more than the dimensions.

Implement `sae_loss(params, X, l1)` with `params = (W_e, b_e, W_d, b_d)`, returning the loss and the gradients in the same order.

## Hints

1. Backpropagate: $\partial \hat x = 2(\hat x - x)/n$; $\partial z = \partial \hat x\, W_d^\top + \lambda/n$; through the ReLU only where the pre-activation is positive.
2. $b_d$ appears twice: added to the output and subtracted from the input.
3. The L1 term is what makes most latents zero for any one input.
