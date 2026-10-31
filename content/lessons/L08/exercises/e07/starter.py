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
    n, d = Q.shape
    c = 1.0 / np.sqrt(d)
    O = np.zeros((n, V.shape[1]))
    L = np.zeros(n)
    for i in range(0, n, Br):
        q = Q[i:i + Br]
        m = np.full(len(q), -np.inf)
        l = np.zeros(len(q))
        acc = np.zeros((len(q), V.shape[1]))
        for j in range(0, n, Bc):
            s = q @ K[j:j + Bc].T * c
            m_new = np.maximum(m, s.max(axis=1))
            p = np.exp(s - m_new[:, None])
            alpha = np.exp(m - m_new)
            l = l * alpha + p.sum(axis=1)
            acc = acc * alpha[:, None] + p @ V[j:j + Bc]
            m = m_new
        O[i:i + Br] = acc / l[:, None]
        L[i:i + Br] = m + np.log(l)
    return O, L


def flash_backward(dO, Q, K, V, O, L, Bc=4):
    """Backward pass that recomputes each block of probabilities from the stored log-sum-exp L:
    P_ij = exp(S_ij - L_i), with D_i = rowsum(dO_i * O_i). Return (dQ, dK, dV)."""
    raise NotImplementedError
