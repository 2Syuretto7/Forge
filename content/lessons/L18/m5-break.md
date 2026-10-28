# Break it: hangs and wrong averages

## Collectives that never complete

::::predict{id=p4 kind=choice answer=d}
On one of 8 GPUs the loss comes out NaN, and the training loop's guard `if loss.isnan(): continue` skips that step on that GPU only. What happens?

- That GPU's update is skipped and training continues normally.
- The other GPUs average 7 gradients instead of 8.
- An exception is raised on every GPU.
- The other seven GPUs wait forever in their all-reduce, and the job hangs.

:::reveal
A collective completes only when every rank calls it. The rank that skipped moves on to the next step's forward pass while the other seven block in the gradient all-reduce, and from then on the ranks issue their collectives out of step. Nothing crashes; the job just stops making progress until a timeout kills it. Decisions that change which collectives run must be made together, with a collective of their own.
:::
::::

:::exercise{ref=e11}
:::

## Averages that are not

:::exercise{ref=e12}
:::

## What to take away

- Count the bytes before you launch: model states, activations, then the margin for everything else.
- Put tensor parallelism where the links are fastest, pipelines across servers, data parallelism outside.
- Every rank must call the same collectives in the same order; make any skip decision with a collective.
- Average gradients over examples, not over ranks, and check that the effective learning rate does not change with the number of GPUs.
