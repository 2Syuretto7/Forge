# Recall bridge: kernels, attention and low precision

From L12: a kernel's speed is set by the bytes it moves as much as by its FLOPs. From L13: attention compares each position's query with every earlier key. From L17: fewer bits per number means fewer bytes to move. Serving a trained model puts all three together: generation reads the whole model for every token it produces, so inference is a memory problem first. Reviews due from L12, L13 and L17 appear above.

::::derivation{id=d0 title="Warm-up"}
:::step
A model with 6.74 billion parameters in 16-bit precision takes about [[13.48|tol=0.01]] GB.
:::
:::step
Reading it once from a GPU with 2 TB/s of bandwidth takes about [[6.74|tol=0.01]] ms.
:::
:::step
So one sequence decodes at most about [[148|tol=1]] tokens per second, however fast the arithmetic is.
:::
::::
