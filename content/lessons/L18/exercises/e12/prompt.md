# Break it: outliers

Large language models develop a few input features with huge activations (Dettmers et al., 2022). With one scale for the whole matrix, those features' weights set the scale and every other weight rounds to almost nothing.

1. `per_tensor_int8(W)`: one scale for the matrix; return the dequantized weights.
2. `mixed_precision_int8(W, X, k)`: keep the `k` input features (columns of $W$) with the largest mean absolute activation in $X$ in full precision, and quantize the rest per output row (the LLM.int8 recipe).

## Hints

1. Rank features by `np.abs(X).mean(axis=0)`.
2. Quantize the remaining columns with per-row scales as in exercise 7.
3. Keeping a handful of columns in 16 bits costs little memory and removes most of the error.
