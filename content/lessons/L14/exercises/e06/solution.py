import numpy as np


def bigram_probs(ids, V, alpha=1.0):
    """P[a, b] = (count(a followed by b) + alpha) / (count(a followed by anything) + alpha V)."""
    C = np.zeros((V, V))
    np.add.at(C, (np.asarray(ids[:-1]), np.asarray(ids[1:])), 1.0)
    return (C + alpha) / (C.sum(axis=1, keepdims=True) + alpha * V)


def cross_entropy(ids, P):
    """Mean of -ln P[ids[t], ids[t+1]] over the sequence: nats per token."""
    a, b = np.asarray(ids[:-1]), np.asarray(ids[1:])
    return float(-np.mean(np.log(P[a, b])))


def perplexity(nats_per_token):
    return float(np.exp(nats_per_token))


def bits_per_char(nats_per_token, n_tokens, n_chars):
    """Convert a per-token loss to bits per character of the underlying text."""
    return nats_per_token * n_tokens / n_chars / np.log(2)
