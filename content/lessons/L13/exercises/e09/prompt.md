# Parameters and FLOPs of a GPT

1. `gpt_params(vocab, n_ctx, d, n_layer)`: the GPT-2 layout. Token embeddings ($V \times d$) and position embeddings ($n_{\text{ctx}} \times d$); per block a fused query-key-value projection $d \times 3d$ with bias, an output projection $d \times d$ with bias, an MLP $d \times 4d$ and $4d \times d$ with biases, and two layer norms ($2d$ each); a final layer norm; and an output layer that reuses the token embedding matrix, adding nothing.
2. `forward_flops_per_token(d, n_layer, n_ctx)`: $2 \cdot 12 d^2$ per layer for the weights plus $4 n_{\text{ctx}} d$ per layer for attention (scores and weighted values, counting the full $n \times n$ products).
3. `attention_crossover_ctx(d)`: the context length at which the two terms are equal.

The tests check your count against GPT-2 small: 124,439,808 parameters.

## Hints

1. Each block: $(3d^2 + 3d) + (d^2 + d) + (4d^2 + 4d) + (4d^2 + d) + 4d$.
2. GPT-2 small: vocabulary 50257, context 1024, width 768, 12 layers.
3. Set $4nd = 24d^2$ and solve for $n$.
