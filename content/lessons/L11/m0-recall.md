# Recall bridge: the operations on the tape

From L08: an autograd engine records every tensor operation and replays a backward rule for each. On a GPU, each of those operations becomes at least one **kernel**, a function that thousands of GPU threads run in parallel. This lesson is about what such a kernel costs. Reviews due from L08 appear above.

::::derivation{id=d0 title="Warm-up"}
:::step
A matrix product of a $64 \times 512$ matrix with a $512 \times 512$ matrix costs $2 \cdot 64 \cdot 512 \cdot 512 =$ [[33554432]] FLOPs (each multiply-add counts as two).
:::
:::step
Its backward pass computes two matrix products of the same size, so it costs [[2]] times the forward pass.
:::
:::step
Adding two vectors of $10^6$ fp32 numbers reads two vectors and writes one, moving $3 \cdot 4 \cdot 10^6 =$ [[12000000]] bytes for $10^6$ FLOPs.
:::
::::
