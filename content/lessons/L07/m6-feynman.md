# Explain it plainly: memory-bound and compute-bound

Explain to a programmer who has just moved a training loop from CPU to GPU why some operations got a hundred times faster and others barely changed.

- Write 150 to 400 words.
- Use a concrete comparison between a matrix product and an elementwise operation.
- Explain arithmetic intensity and what decides whether a kernel is memory-bound.
- Mention one practical fix for a memory-bound or launch-bound workload.

:::feynman{id=f1 prompt="Explain why a matrix multiplication runs close to a GPU's peak FLOP rate while an elementwise operation runs far below it, using arithmetic intensity and the roofline model, and give one practical fix for memory-bound or launch-bound code." key_points="A kernel is limited by whichever is slower, computing its FLOPs or moving its bytes|Arithmetic intensity is FLOPs per byte moved; a matmul's grows with matrix size while an elementwise operation's stays below one|Kernels below the ridge point, peak FLOPs divided by bandwidth, are memory-bound and gain nothing from more compute|Small kernels can be dominated by launch overhead and synchronization rather than by either limit|A concrete fix such as fusion, larger batches, lower precision or avoiding per-step synchronization"}
:::
