import numpy as np


def reference_attention(Q, K, V):
    S = Q @ K.T / np.sqrt(Q.shape[1])
    P = np.exp(S - S.max(axis=1, keepdims=True))
    P /= P.sum(axis=1, keepdims=True)
    return P @ V


def flash_attention(Q, K, V, Br=4, Bc=4):
    """Tiled attention: for each block of Br queries, loop over blocks of Bc keys and values with an
    online softmax, never forming the full score matrix. Return (O, L) with L the log-sum-exp of each
    row of scores (kept for the backward pass)."""
    raise NotImplementedError
