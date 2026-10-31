def count_params(vocab, ctx, d, n_layer):
    """Parameters of the L10 GPT: token and position embeddings, n_layer pre-norm blocks (two
    layer norms, a fused qkv projection, an output projection and a 4d MLP, all with biases), a
    final layer norm, and an output layer tied to the token embedding.
    Return {"total", "non_embedding", "approx"} where non_embedding leaves out both embeddings
    and approx = 12 n_layer d^2."""
    block = 2 * d + (3 * d * d + 3 * d) + (d * d + d) + 2 * d + (4 * d * d + 4 * d) + (4 * d * d + d)
    non_embedding = n_layer * block + 2 * d
    return {
        "total": non_embedding + vocab * d + ctx * d,
        "non_embedding": non_embedding,
        "approx": 12 * n_layer * d * d,
    }
