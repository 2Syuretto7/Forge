import numpy as np


def tied_bigram_loss(E, b, x, y):
    """A neural bigram model with tied embeddings: logits = E[x] E^T + b, softmax cross-entropy
    against y (mean over the batch). The same matrix E embeds the input and scores the output.
    Return (loss, dE, db)."""
    raise NotImplementedError
