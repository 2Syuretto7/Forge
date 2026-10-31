import numpy as np


def fit_unigram(tokens, mask, vocab):
    """Next-token frequencies estimated from the tokens whose mask is 1, with add-one smoothing."""
    raise NotImplementedError


def response_ce(p, tokens, mask):
    """Mean -log p(token) over the tokens whose mask is 1."""
    raise NotImplementedError
