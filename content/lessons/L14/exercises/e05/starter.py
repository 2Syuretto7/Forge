import numpy as np


def adam_update(w, g, m, v, t, lr, b1=0.9, b2=0.999, eps=1e-8):
    """One Adam step (with bias correction) on arrays; return (w, m, v)."""
    raise NotImplementedError


def zero1_step(w, rank_grads, states, t, lr):
    """ZeRO stage 1 over P = len(rank_grads) ranks. Average the gradients, then rank r updates only
    its shard np.array_split(range(len(w)), P)[r] of the weights, using its own (m, v) shard in
    states[r]; the updated shards are gathered into the full weights. Return (w, states)."""
    raise NotImplementedError
