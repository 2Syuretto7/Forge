# Break it: silent resume bugs

The worst failures do not crash. A run that resumes with the wrong data order or the wrong learning rate keeps training, its loss looks plausible, and its results can never be reproduced.

## The data order

:::exercise{ref=e11}
:::

## The schedule

Compare the healthy run with the learning-rate bug in the widget, with the lower panel on the learning rate.

:::widget{name=LossSpikeExplorer run=lr_bug compare=healthy}
:::

::::predict{id=p4 kind=choice answer=a}
A run is resumed at step 3000 of 6000, but its scheduler object is rebuilt without restoring its step count. What happens to the learning rate?

- It goes through warmup again from almost zero and returns to the peak, in the middle of training.
- Nothing: the schedule is stored in the optimizer.
- It stays at the value it had at step 3000.
- It drops to zero.

:::reveal
A scheduler that counts its own calls restarts from zero, so the run repeats warmup and then sits at the peak rate when it should be decaying: a learning-rate bug introduced by a restart. Computing the rate from the step alone (exercise 5), and auditing the logged rates after every resume (exercise 12), removes the bug and catches it.
:::
::::

:::exercise{ref=e12}
:::

## What to take away

- Log the loss, the gradient norm before clipping, the learning rate and throughput every step, and the validation loss with an interval regularly.
- Checkpoint everything the next step depends on, atomically, and test exact resume.
- Detect spikes against a trailing window; recover by restoring a checkpoint before the spike and skipping the data around it.
- After every resume, check the data order and the learning rate against an uninterrupted run.
