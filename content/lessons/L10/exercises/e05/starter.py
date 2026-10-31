import numpy as np


def train_val_split(ids, frac=0.9):
    """The first frac of the tokens for training, the rest for validation (never shuffled across)."""
    raise NotImplementedError


def get_batch(ids, ctx, batch, rng):
    """batch random windows: x[b] = ids[s:s + ctx] and y[b] = ids[s + 1:s + ctx + 1], with starts
    drawn by rng.integers(0, len(ids) - ctx, size=batch)."""
    raise NotImplementedError


def tokens_per_epoch(n_tokens, ctx, batch):
    """Training steps per pass over the data, if every window position is used once: n / (ctx * batch)."""
    raise NotImplementedError
