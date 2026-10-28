# Capstone: the GPT in mixed precision

In the notebook, read the formats' limits from `torch.finfo`, then train the same GPT twice from identical weights: once in fp32 and once with `torch.autocast` in fp16 and a `GradScaler`. The final losses must agree within 3 percent, and on a T4 the mixed-precision run must be at least 1.5 times faster and use less memory.

:::exercise{ref=capstone}
:::

:::colab{notebook=L17}
:::

## When you finish

Sixteen bytes per parameter, and activations on top, will not fit one GPU for a large model. L18 splits them across many.

:::edge{to=L18 text="Split the 16 bytes per parameter across GPUs."}
:::
