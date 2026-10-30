# Counting FLOPs by counting

Section 6 claimed that multiplying an $m \times n$ matrix by a vector costs $2mn$ FLOPs. Check it by counting.

- `matvec(W, x)` multiplies a matrix given as a list of rows by a list `x`, with explicit loops (no NumPy), and returns `(y, flops)` where `y` is the list of outputs and `flops` counts every multiplication and every addition you perform. Start each output's running total at `0.0` and add each product to it, so each output costs `n` multiplications and `n` additions.
- `mlp_flops(widths, batch=1)` returns the FLOPs of a forward pass through a stack of dense layers with the given widths (for `[784, 512, 10]` there are two weight matrices, 784 by 512 and 512 by 10), for `batch` inputs, counting $2 \times$ inputs $\times$ outputs per layer per input.
- `mlp_params(widths)` counts weights and biases: each layer has `inputs * outputs` weights and `outputs` biases.
- `train_flops(n_params, n_tokens)` returns $6ND$.

## Hints

1. Two nested `for` loops: over rows `i`, then over columns `j`, with `acc = acc + W[i][j] * x[j]` and `flops += 2`.
2. `zip(widths[:-1], widths[1:])` pairs each width with the next.
3. The tests compare `matvec` against NumPy and `flops` against `2 * m * n`.
