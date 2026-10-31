import numpy as np


def softmax(z):
    e = np.exp(z - z.max(axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)


def attention(x, Wq, Wk, Wv, Wo, heads):
    """Dense causal multi-head attention for one sequence x of shape (T, d)."""
    T, d = x.shape
    hd = Wq.shape[1] // heads
    mask = np.triu(np.ones((T, T), dtype=bool), 1)
    outs = []
    for h in range(heads):
        sl = slice(h * hd, (h + 1) * hd)
        s = (x @ Wq[:, sl]) @ (x @ Wk[:, sl]).T / np.sqrt(hd)
        outs.append(softmax(np.where(mask, -np.inf, s)) @ (x @ Wv[:, sl]))
    return np.concatenate(outs, axis=1) @ Wo


def shard_attention(Wq, Wk, Wv, Wo, heads, tp):
    """Split the weights over tp ranks by heads: rank r gets the columns of Wq, Wk, Wv for heads
    r * heads / tp .. (r + 1) * heads / tp - 1, and the matching rows of Wo. Return a list of tp
    tuples (Wq_r, Wk_r, Wv_r, Wo_r)."""
    hd = Wq.shape[1] // heads
    per = heads // tp
    out = []
    for r in range(tp):
        sl = slice(r * per * hd, (r + 1) * per * hd)
        out.append((Wq[:, sl], Wk[:, sl], Wv[:, sl], Wo[sl, :]))
    return out


def tp_attention(x, shards, heads_per_rank):
    """Every rank runs attention over its own heads and multiplies by its rows of Wo; one
    all-reduce (a sum) of the partial outputs gives the full result."""
    return sum(attention(x, Wq, Wk, Wv, Wo, heads_per_rank) for Wq, Wk, Wv, Wo in shards)
