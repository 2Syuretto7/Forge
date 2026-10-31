# Capstone: train a transformer on Shakespeare

In the notebook, write causal multi-head attention, the pre-norm block and the model in PyTorch, check your attention against PyTorch's fused implementation, check causality by perturbation, and train a two-layer model on about a megabyte of Shakespeare to a validation loss below 1.70 nats per character. With the reference settings this takes about a minute on a T4.

:::exercise{ref=capstone}
:::

:::colab{notebook=L09}
:::

## When you finish

Your model reads characters. L10 builds a byte-pair tokenizer, a proper data pipeline and sampling controls, and turns the same architecture into a small GPT; L08 rewrites its attention as one fused kernel.

:::edge{to=L10 text="Add a tokenizer and a data pipeline: a GPT from scratch."}
:::

:::edge{to=L16 text="Fine-tuning adapts these projection matrices."}
:::

:::edge{to=L19 text="What individual heads learn to do."}
:::
