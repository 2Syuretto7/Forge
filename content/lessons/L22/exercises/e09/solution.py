import numpy as np


def emitted_distribution(p, q):
    """Speculative decoding's rule for one token: draw x from the draft q, accept it with
    probability min(1, p(x)/q(x)), otherwise draw from max(0, p - q) renormalized. Return the
    exact distribution of the emitted token."""
    p, q = np.asarray(p, dtype=float), np.asarray(q, dtype=float)
    accept = np.minimum(q, p)
    residual = np.maximum(p - q, 0)
    reject_mass = 1 - accept.sum()
    out = accept.copy()
    if residual.sum() > 0:
        out += reject_mass * residual / residual.sum()
    return out


def acceptance_rate(p, q):
    """The probability the draft's token is accepted: sum min(p, q) = 1 - total variation."""
    return float(np.minimum(p, q).sum())


def acceptance_grad(p, z):
    """The gradient of acceptance_rate(p, softmax(z)) with respect to the draft's logits z."""
    q = np.exp(z - z.max())
    q /= q.sum()
    g = (q < p).astype(float)  # d min(p, q) / d q
    return q * (g - q @ g)


def expected_tokens(alpha, gamma):
    """Tokens produced per target-model call when gamma draft tokens are each accepted with
    probability alpha: (1 - alpha^(gamma + 1)) / (1 - alpha)."""
    return gamma + 1 if alpha == 1 else (1 - alpha ** (gamma + 1)) / (1 - alpha)
