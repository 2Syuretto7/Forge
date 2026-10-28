import numpy as np


def fused_cross_entropy(logits, y, block=8):
    """Mean cross-entropy computed per row in one pass over vocabulary blocks with a running max and
    sum (no full softmax array), and its gradient (softmax - onehot) / B written once.
    Return (loss, dlogits)."""
    B, V = logits.shape
    lse = np.zeros(B)
    for r in range(B):
        m, l = -np.inf, 0.0
        for s in range(0, V, block):
            b = logits[r, s:s + block]
            m_new = max(m, float(b.max()))
            l = l * np.exp(m - m_new) + float(np.exp(b - m_new).sum())
            m = m_new
        lse[r] = m + np.log(l)
    loss = float(np.mean(lse - logits[np.arange(B), y]))
    d = np.exp(logits - lse[:, None])
    d[np.arange(B), y] -= 1.0
    return loss, d / B
