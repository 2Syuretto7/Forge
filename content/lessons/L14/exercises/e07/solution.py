import numpy as np


def tied_bigram_loss(E, b, x, y):
    """A neural bigram model with tied embeddings: logits = E[x] E^T + b, softmax cross-entropy
    against y (mean over the batch). The same matrix E embeds the input and scores the output.
    Return (loss, dE, db)."""
    h = E[x]
    Z = h @ E.T + b
    Z = Z - Z.max(axis=1, keepdims=True)
    logp = Z - np.log(np.exp(Z).sum(axis=1, keepdims=True))
    n = len(x)
    loss = -float(np.mean(logp[np.arange(n), y]))
    G = np.exp(logp)
    G[np.arange(n), y] -= 1.0
    G /= n
    dE = G.T @ h
    np.add.at(dE, x, G @ E)
    return loss, dE, G.sum(axis=0)
