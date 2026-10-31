def count_params(vocab, ctx, d, n_layer):
    """Parameters of the L10 GPT: token and position embeddings, n_layer pre-norm blocks (two
    layer norms, a fused qkv projection, an output projection and a 4d MLP, all with biases), a
    final layer norm, and an output layer tied to the token embedding.
    Return {"total", "non_embedding", "approx"} where non_embedding leaves out both embeddings
    and approx = 12 n_layer d^2."""
    raise NotImplementedError
