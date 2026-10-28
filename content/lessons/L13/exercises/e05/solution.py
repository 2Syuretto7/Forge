import numpy as np


def softmax_rows(S):
    """Softmax of every row, stable for large entries; -inf entries get weight 0."""
    m = S.max(axis=-1, keepdims=True)
    E = np.exp(S - m)
    return E / E.sum(axis=-1, keepdims=True)


def softmax_backward(P, dP):
    """Given P = softmax_rows(S) and dL/dP, return dL/dS."""
    return P * (dP - (dP * P).sum(axis=-1, keepdims=True))


def causal_mask(n):
    """Boolean (n, n) array, True where query i may not see key j (j > i)."""
    return np.triu(np.ones((n, n), dtype=bool), k=1)


def attention(Q, K, V, causal=True, scale=True):
    """Single-head attention for Q, K of shape (n, d) and V of shape (n, dv). Return (O, P)."""
    S = Q @ K.T
    if scale:
        S = S / np.sqrt(Q.shape[-1])
    if causal:
        S = np.where(causal_mask(Q.shape[0]), -np.inf, S)
    P = softmax_rows(S)
    return P @ V, P


def attention_backward(dO, Q, K, V, P, scale=True):
    """Gradients of single-head attention given dL/dO and the weights P. Return (dQ, dK, dV)."""
    c = 1.0 / np.sqrt(Q.shape[-1]) if scale else 1.0
    dV = P.T @ dO
    dP = dO @ V.T
    dS = softmax_backward(P, dP) * c
    return dS @ K, dS.T @ Q, dV


def split_heads(X, h):
    """(n, d) -> (h, n, d // h): head i gets columns i * d/h to (i + 1) * d/h."""
    n, d = X.shape
    return X.reshape(n, h, d // h).transpose(1, 0, 2)


def merge_heads(Y):
    """(h, n, dh) -> (n, h * dh), the inverse of split_heads."""
    h, n, dh = Y.shape
    return Y.transpose(1, 0, 2).reshape(n, h * dh)


def mha_forward(X, Wq, Wk, Wv, Wo, h, causal=True):
    """Multi-head self-attention: project, split into h heads, attend per head, merge, project.
    Return (Y, cache)."""
    Q, K, V = split_heads(X @ Wq, h), split_heads(X @ Wk, h), split_heads(X @ Wv, h)
    outs, Ps = [], []
    for i in range(h):
        O, P = attention(Q[i], K[i], V[i], causal=causal)
        outs.append(O)
        Ps.append(P)
    M = merge_heads(np.stack(outs))
    return M @ Wo, (X, Q, K, V, np.stack(Ps), M)


def mha_backward(dY, cache, Wq, Wk, Wv, Wo):
    """Return (dX, dWq, dWk, dWv, dWo)."""
    X, Q, K, V, P, M = cache
    h = Q.shape[0]
    dWo = M.T @ dY
    dO = split_heads(dY @ Wo.T, h)
    dQ, dK, dV = np.zeros_like(Q), np.zeros_like(K), np.zeros_like(V)
    for i in range(h):
        dQ[i], dK[i], dV[i] = attention_backward(dO[i], Q[i], K[i], V[i], P[i])
    dQm, dKm, dVm = merge_heads(dQ), merge_heads(dK), merge_heads(dV)
    dX = dQm @ Wq.T + dKm @ Wk.T + dVm @ Wv.T
    return dX, X.T @ dQm, X.T @ dKm, X.T @ dVm, dWo
