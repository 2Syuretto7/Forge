# Capstone: FlashAttention in Triton

The notebook takes you from a vector-add kernel to a fused softmax, a tiled matrix multiplication, a fused layer norm and the forward pass of FlashAttention. Your FlashAttention must match unfused attention within $10^{-2}$ in fp16 and run faster than it at sequence length 2048 on a T4. Without a GPU the kernels run in Triton's interpreter, slowly but exactly, which is the easiest way to debug them.

:::exercise{ref=capstone}
:::

:::colab{notebook=L12}
:::

## When you finish

You have written the kernel at the center of modern transformers. L22 adds what inference needs on top: keys and values cached from earlier steps, stored in pages, and attention over them for many requests at once.

:::edge{to=L22 text="Inference: cached keys and values and paged attention."}
:::
