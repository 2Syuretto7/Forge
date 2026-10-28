import numpy as np


def bigram_probs(ids, V, alpha=1.0):
    """P[a, b] = (count(a followed by b) + alpha) / (count(a followed by anything) + alpha V)."""
    raise NotImplementedError


def cross_entropy(ids, P):
    """Mean of -ln P[ids[t], ids[t+1]] over the sequence: nats per token."""
    raise NotImplementedError


def perplexity(nats_per_token):
    raise NotImplementedError


def bits_per_char(nats_per_token, n_tokens, n_chars):
    """Convert a per-token loss to bits per character of the underlying text."""
    raise NotImplementedError
