import numpy as np

# A hand-built two-layer network computing "does token A come before token B?" from one-hot inputs.
W1 = np.zeros((4, 6))
W1[0, 0] = 1.0   # unit 0: A at position 0
W1[1, 3] = 1.0   # unit 1: B at position 1
W1[2, 1] = 1.0   # unit 2: a distractor
W1[3, 4] = 0.5   # unit 3: another distractor
w2 = np.array([1.0, 1.0, 0.1, 0.1])


def hidden(x):
    return np.maximum(W1 @ x, 0)


def output(h):
    return w2 @ h - 1.5  # positive exactly when units 0 and 1 are both on


def patch_effects(x_clean, x_corrupt):
    """Activation patching: run the corrupted input, but replace one hidden unit's value with its
    value on the clean input; the effect of that unit is how much of the clean-minus-corrupted
    output difference this restores. Return the fraction restored for each unit."""
    raise NotImplementedError
