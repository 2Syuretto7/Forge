# Capstone: profile and fix a slow training step

The notebook benchmarks the T4, then hands you a training step that is correct and slow. Profile it with `torch.profiler`, find where its time goes, and write a version that is at least twice as fast and produces the same losses. Use a T4 runtime: the speedup test only runs on a GPU.

:::exercise{ref=capstone}
:::

:::colab{notebook=L07}
:::

## When you finish

You have measured the two roofs and the overheads around them. L08 attacks the memory roof directly: you will write fused kernels in Triton, including FlashAttention, which turns attention from memory-bound to compute-bound.

:::edge{to=L08 text="Write the fused kernels yourself."}
:::
