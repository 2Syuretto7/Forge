# Counting parameters

Implement `count_params(vocab, ctx, d, n_layer)` for the L10 GPT. Return a dictionary with:

- `"total"`: every parameter, with the output layer tied to the token embedding (so it adds none);
- `"non_embedding"`: everything except the token and position embeddings;
- `"approx"`: the rule of thumb $12\,n_\text{layer}\,d^2$.

Each block has two layer norms (a weight and a bias of size $d$ each), a fused $d \to 3d$ projection, a $d \to d$ output projection, and an MLP $d \to 4d \to d$; every linear layer has a bias. A final layer norm follows the blocks.

## Hints

1. A linear layer from $m$ to $n$ features has $mn + n$ parameters; a layer norm over $d$ features has $2d$.
2. One block has $12d^2 + 13d$ parameters.
3. Scaling laws use the non-embedding count: embeddings are lookups, not matrix multiplications, and contribute almost no FLOPs.
