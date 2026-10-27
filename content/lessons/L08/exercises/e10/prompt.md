# What the tape keeps alive

The table `SAVES` in the starter records what each operation's backward rule needs from the forward pass: `"inputs"` (all inputs), `"input"` (the first input), `"output"`, or `"output_probs"` (for the fused cross-entropy: the probabilities, which have the shape of the logits).

1. `graph_nodes(t)`: every tensor reachable from `t` through parents, including `t`, each once.
2. `saved_bytes(loss)`: the total bytes those saved arrays occupy for the graph ending at `loss`, by the table. Count by the arrays' `nbytes` (float64, 8 bytes per value).
3. `mlp_saved_bytes_formula(sizes, B)`: the same number predicted in closed form for `MLP(sizes)` on a batch of `B` with `cross_entropy_fused`, without building a graph.

Then use them: compare the saved bytes with the parameter bytes for a wide, shallow network at batch 256.

## Hints

1. `graph_nodes`: a stack and a set of `id`s.
2. A linear layer contributes its matmul (saves `x` and `W`, so $8(Ba + ab)$ bytes); the add of the bias saves nothing; each ReLU saves its input, $8Bb$.
3. The fused cross-entropy saves probabilities of shape `(B, C)`.
