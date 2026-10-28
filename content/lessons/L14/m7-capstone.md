# Capstone: a GPT with its own tokenizer

In the notebook you train a byte-level BPE tokenizer with 512 tokens on Shakespeare, encode the corpus, train a four-layer GPT with tied embeddings on the tokens, report the validation loss in nats per token and in bits per character, and write the sampling filters. The target is below 2.3 bits per character; the reference settings reach it in a few minutes on a T4.

:::exercise{ref=capstone}
:::

:::colab{notebook=L14}
:::

## When you finish

You can now train a language model end to end. L15 asks how its loss changes with more parameters, more data and more compute; L16 asks what data to feed it; L17 makes the same training run faster in reduced precision.

:::edge{to=L15 text="How the loss scales with parameters, data and compute."}
:::

:::edge{to=L16 text="Which data, and how to prepare it at scale."}
:::
