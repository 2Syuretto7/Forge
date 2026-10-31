# Break it: a resume that changes the data order

`batch_ids(seed, epoch, n, batch_size)` gives an epoch's batches as tuples of example ids. `buggy_resume` shows a common mistake: after a restart in the middle of an epoch it starts that epoch over, so the run sees the epoch's first batches twice and the rest of the data at different steps than the original run.

1. `stream(seed, epoch, batch_index, n, batch_size, count)`: the correct continuation, `count` batches from `batch_index` of `epoch` onward.
2. `first_divergence(reference, resumed)`: the first position where two batch sequences differ, or `None`.

## Hints

1. Slice the first epoch's batches from `batch_index`; later epochs start at 0.
2. To test a resume, record the batch ids of an uninterrupted run and compare.
3. Nothing crashes with the buggy resume and the loss looks fine: only a comparison like this one reveals it.
