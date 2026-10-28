import numpy as np
import math


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


C = math.sqrt(2.0 / math.pi)


def gelu(x):
    return 0.5 * x * (1.0 + np.tanh(C * (x + 0.044715 * x ** 3)))


def layernorm(x, g, b, eps=1e-5):
    mu = x.mean(axis=-1, keepdims=True)
    var = x.var(axis=-1, keepdims=True)
    return g * (x - mu) / np.sqrt(var + eps) + b


def init_block(d, seed=0):
    rng = np.random.default_rng(seed)
    w = lambda a, b: rng.normal(size=(a, b)) * 0.02
    return {
        "ln1_g": np.ones(d), "ln1_b": np.zeros(d),
        "Wq": w(d, d), "Wk": w(d, d), "Wv": w(d, d), "Wo": w(d, d), "bo": np.zeros(d),
        "ln2_g": np.ones(d), "ln2_b": np.zeros(d),
        "W1": w(d, 4 * d), "b1": np.zeros(4 * d), "W2": w(4 * d, d), "b2": np.zeros(d),
    }


def block_forward(X, p, h):
    """Pre-norm decoder block: X + MHA(LN1(X)), then + MLP(LN2(.)) with a 4d GELU hidden layer."""
    raise NotImplementedError


def block_param_count(d):
    """Parameters of one block as created by init_block: four d x d attention matrices, the output
    bias, the two MLP matrices with their biases, and two layer norms."""
    raise NotImplementedError
