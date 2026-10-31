# Detecting a spike

1. `detect_spikes(losses, window, k)`: the 1-based steps whose loss exceeds the mean of the previous `window` losses by more than $k$ of their standard deviations. A non-finite loss always counts; no step is flagged before a full window exists.
2. `rollback_point(flagged_step, checkpoint_every)`: the step of the checkpoint to restore. The loss at step $s$ is computed before update $s$, so update $s - 1$ may already be damaged: use the last checkpoint saved before it.

## Hints

1. `np.isfinite` catches NaN and infinity, which compare false with everything.
2. A trailing window adapts to the falling loss; a fixed threshold would fire early in training and never late.
3. The rollback step is $\lfloor (s - 2)/c \rfloor \cdot c$.
