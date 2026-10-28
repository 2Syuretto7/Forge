# The decoder block

Multi-head attention, `gelu`, `layernorm` and `init_block(d)` (which creates the block's parameters) are provided.

1. `block_forward(X, p, h)`: the pre-norm block. First $X \leftarrow X + \operatorname{MHA}(\operatorname{LN}_1(X)) + b_o$, then $X \leftarrow X + \operatorname{gelu}(\operatorname{LN}_2(X) W_1 + b_1) W_2 + b_2$, with causal attention.
2. `block_param_count(d)`: the number of parameters `init_block(d)` creates, as a formula in $d$.

## Hints

1. Call `mha_forward(layernorm(X, ...), Wq, Wk, Wv, Wo, h)` and keep only its output.
2. Count: four $d \times d$ attention matrices, two $d \times 4d$ MLP matrices, biases of sizes $d$, $4d$ and $d$, and two layer norms with $2d$ each.
3. The block must stay causal: its output at position $t$ cannot depend on later positions.
