import numpy as np


def detect_spikes(losses, window, k):
    """1-based steps whose loss exceeds the mean of the previous `window` losses by more than k of
    their standard deviations (a non-finite loss always counts). Steps before a full window are
    never flagged."""
    out = []
    for i in range(window, len(losses)):
        prev = np.asarray(losses[i - window:i], dtype=float)
        if not np.isfinite(losses[i]) or losses[i] > prev.mean() + k * prev.std():
            out.append(i + 1)
    return out


def rollback_point(flagged_step, checkpoint_every):
    """The loss at step s is measured before update s, so update s - 1 may already be damaged:
    return the last checkpoint step saved before it (checkpoints are saved after steps
    checkpoint_every, 2 checkpoint_every, ...; step 0 is the initialization)."""
    return (flagged_step - 2) // checkpoint_every * checkpoint_every
