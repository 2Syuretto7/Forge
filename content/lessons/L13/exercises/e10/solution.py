def score_bytes(batch, heads, n_ctx, bytes_per=2):
    """Memory of one layer's attention weights P (batch x heads x n_ctx x n_ctx)."""
    return batch * heads * n_ctx * n_ctx * bytes_per


def scores_intensity(n_ctx, d_head, bytes_per=2):
    """S = Q K^T for one head: 2 n^2 d FLOPs; reads Q and K (n x d each), writes S (n x n)."""
    return 2 * n_ctx * n_ctx * d_head / (bytes_per * (2 * n_ctx * d_head + n_ctx * n_ctx))


def max_ctx_for_memory(budget_bytes, batch, heads, bytes_per=2):
    """Largest n_ctx whose attention weights for one layer fit in the budget."""
    return int((budget_bytes / (batch * heads * bytes_per)) ** 0.5)
