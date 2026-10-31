# Puzzle: eight GPUs, one model

You have eight GPUs with 80 GB each and a 7-billion-parameter model that needs 112 GB of model states.

::::predict{id=p1 kind=choice answer=c}
Plain data parallelism copies the whole model to every GPU and averages gradients. Does it fit?

- Yes: eight GPUs have 640 GB between them.
- Yes, if the batch is small enough.
- No: every GPU still holds all 112 GB of model states.
- No, because gradients cannot be averaged across GPUs.

:::reveal
Data parallelism splits the **batch**, not the model: every GPU keeps a full copy of weights, gradients and optimizer states. To use the pooled memory you must shard the model states (ZeRO), split the layers' matrices (tensor parallelism) or split the layers themselves (pipeline parallelism). The widget below adds up the memory per GPU for any combination.
:::
::::

:::widget{name=ParallelismPlanner model=b6_7 dp=3}
:::

::::predict{id=p2 kind=choice answer=b}
Averaging 1 GB of gradients across 8 GPUs with a ring all-reduce, how much does each GPU send?

- 8 GB: one copy to every other GPU.
- 1.75 GB.
- 0.125 GB: its eighth of the data.
- 1 GB.

:::reveal
A ring all-reduce is a reduce-scatter followed by an all-gather. Each moves $(P-1)/P$ of the data through every GPU, so each sends $2 \cdot 7/8 = 1.75$ GB, and that amount barely changes as you add GPUs. The cost of averaging gradients is set by the model size and the link bandwidth, not by the number of GPUs.
:::
::::
