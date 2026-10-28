import numpy as np


def softmax_rows(S):
    """Softmax of every row, stable for large entries; -inf entries get weight 0."""
    m = S.max(axis=-1, keepdims=True)
    E = np.exp(S - m)
    return E / E.sum(axis=-1, keepdims=True)


def softmax_backward(P, dP):
    """Given P = softmax_rows(S) and dL/dP, return dL/dS."""
    return P * (dP - (dP * P).sum(axis=-1, keepdims=True))


def leaks_future(attn_fn, X, eps=1e-3):
    """attn_fn maps an (n, d) sequence to an (n, d) output. Perturb each position t in turn and report
    whether any output at a position before t changes (by more than 1e-12)."""
    raise NotImplementedError


def off_by_one_mask(n):
    """The bug: masking j > i + 1 instead of j > i, so each position also sees the next one."""
    raise NotImplementedError
