import numpy as np


def adam_update(w, g, m, v, t, lr, b1=0.9, b2=0.999, eps=1e-8):
    """One Adam step (with bias correction) on arrays; return (w, m, v)."""
    m = b1 * m + (1 - b1) * g
    v = b2 * v + (1 - b2) * g * g
    w = w - lr * (m / (1 - b1 ** t)) / (np.sqrt(v / (1 - b2 ** t)) + eps)
    return w, m, v


def zero1_step(w, rank_grads, states, t, lr):
    """ZeRO stage 1 over P = len(rank_grads) ranks. Average the gradients, then rank r updates only
    its shard np.array_split(range(len(w)), P)[r] of the weights, using its own (m, v) shard in
    states[r]; the updated shards are gathered into the full weights. Return (w, states)."""
    P = len(rank_grads)
    g = sum(rank_grads) / P
    parts = np.array_split(np.arange(len(w)), P)
    new_w = np.empty_like(w)
    new_states = []
    for r, idx in enumerate(parts):
        m, v = states[r]
        new_w[idx], m, v = adam_update(w[idx], g[idx], m, v, t, lr)
        new_states.append((m, v))
    return new_w, new_states
