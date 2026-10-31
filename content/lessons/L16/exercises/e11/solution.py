import numpy as np


def fit_unigram(tokens, mask, vocab):
    """Next-token frequencies estimated from the tokens whose mask is 1, with add-one smoothing."""
    counts = np.bincount(np.asarray(tokens)[np.asarray(mask) == 1], minlength=vocab) + 1.0
    return counts / counts.sum()


def response_ce(p, tokens, mask):
    """Mean -log p(token) over the tokens whose mask is 1."""
    t = np.asarray(tokens)[np.asarray(mask) == 1]
    return float(-np.mean(np.log(p[t])))
