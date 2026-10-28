import numpy as np


def detect_spikes(losses, window, k):
    """1-based steps whose loss exceeds the mean of the previous `window` losses by more than k of
    their standard deviations (a non-finite loss always counts). Steps before a full window are
    never flagged."""
    raise NotImplementedError


def rollback_point(flagged_step, checkpoint_every):
    """The loss at step s is measured before update s, so update s - 1 may already be damaged:
    return the last checkpoint step saved before it (checkpoints are saved after steps
    checkpoint_every, 2 checkpoint_every, ...; step 0 is the initialization)."""
    raise NotImplementedError
