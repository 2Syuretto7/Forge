# Capstone: teach a pretrained model two tasks without making it forget

The notebook pretrains a small byte-level GPT on Tiny Shakespeare for a few minutes: it knows spelling and the shape of the plays, and follows no instructions. You teach it two tasks from instruction examples, writing a word in capitals (`UPPER: crown` gives `CROWN`) and spelling it backwards (`REVERSE: crown` gives `nworc`). You write the example encoding with its loss mask, the masked loss, the LoRA layer and its merge. The same batches then train LoRA adapters on every linear layer and, for comparison, every weight of the model, both with pretraining text replayed alongside the instructions. Each is scored on 300 words it never saw, with bootstrap intervals, and on how much its loss on held-out Shakespeare rose.

The autograder checks the encoding, the masked loss and the LoRA layer on small cases, that the adapters train under 15% of the parameters and merge into the weights exactly, that LoRA reaches **80%** mean exact-match accuracy on the unseen words while forgetting at most **0.05** nats per byte, and the report.

:::exercise{ref=capstone}
:::

:::colab{notebook=L20}
:::

## When you finish

You have adapted a model to new tasks while keeping what it knew. L21 starts from a fine-tuned model and improves it further with a reward instead of examples.

:::edge{to=L21 text="Improving a fine-tuned model with a reward."}
:::
