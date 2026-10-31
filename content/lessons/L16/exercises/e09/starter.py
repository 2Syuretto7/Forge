import numpy as np


def packed_attention_mask(lengths):
    """Several examples packed into one sequence: position i may attend to position j only if
    j <= i and both belong to the same example. Return a boolean (T, T) array."""
    raise NotImplementedError


def packed_positions(lengths):
    """Position ids that restart at 0 for every packed example."""
    raise NotImplementedError
