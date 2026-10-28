import numpy as np


def packed_attention_mask(lengths):
    """Several examples packed into one sequence: position i may attend to position j only if
    j <= i and both belong to the same example. Return a boolean (T, T) array."""
    doc = np.repeat(np.arange(len(lengths)), lengths)
    T = len(doc)
    return (doc[:, None] == doc[None, :]) & np.tril(np.ones((T, T), dtype=bool))


def packed_positions(lengths):
    """Position ids that restart at 0 for every packed example."""
    return np.concatenate([np.arange(n) for n in lengths])
