def gpt_params(vocab, n_ctx, d, n_layer):
    """GPT-2 layout: token and position embeddings, n_layer blocks (attention with a fused qkv
    projection and biases, MLP 4d with biases, two layer norms), a final layer norm, and an output
    layer tied to the token embedding (no extra parameters)."""
    raise NotImplementedError


def forward_flops_per_token(d, n_layer, n_ctx):
    """2 FLOPs per non-embedding weight (about 12 d^2 per layer), plus attention over n_ctx
    positions: scores and weighted values cost 2 * n_ctx * d FLOPs each per layer."""
    raise NotImplementedError


def attention_crossover_ctx(d):
    """Context length where the attention term equals the weight term: 4 n d = 24 d^2."""
    raise NotImplementedError
