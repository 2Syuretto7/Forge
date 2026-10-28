# What the error does to the outputs

What matters is not the error in each weight but the error in the layer's outputs on real inputs: $\frac{1}{n}\|X W^\top - X \hat W^\top\|^2$ over calibration inputs $X$. Methods like GPTQ round the weights to minimize this.

1. `output_error(W_hat, W, X)`: that error and its gradient with respect to $\hat W$.
2. `group_quantize(W, bits, group)`: symmetric quantization with one scale per `group` consecutive weights in each row (4-bit with groups of 128 is a common choice).

## Hints

1. With $D = X (W - \hat W)^\top$: the gradient is $-2 D^\top X / n$.
2. The levels of a $b$-bit symmetric code run from $-(2^{b-1} - 1)$ to $2^{b-1} - 1$.
3. Smaller groups mean more scales to store and smaller errors.
