# Break it: a schedule that restarts

A run resumed at step 3000 of 6000 rebuilt its scheduler without restoring its step count, so the learning rate went through warmup again, from a tiny value back up to the peak, in the middle of training. The rates were logged, so the bug is visible.

1. `expected_lr(step, peak, warmup, total, floor=0.1)`: the schedule of exercise 5.
2. `audit_lr(logged, peak, warmup, total, rtol=1e-6)`: given (step, lr) pairs from a log, the first step whose rate differs from the schedule by more than `rtol` relative, or `None`.

## Hints

1. Recompute the expected rate for every logged step from the step alone.
2. Run the audit on every resumed run: it costs nothing and catches the restart at its first step.
3. The safest fix is not to have scheduler state at all: compute the rate from the step, as in exercise 5.
