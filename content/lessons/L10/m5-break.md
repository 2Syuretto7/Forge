# Break it: tokenizer edge cases and extreme temperatures

## Strings that break tokenizers

Whitespace, unusual Unicode and normalization are where tokenizers misbehave: two strings that look identical can be different byte sequences, and leading spaces change how words are split.

:::exercise{ref=e11}
:::

## Too cold, too hot

::::predict{id=p5 kind=choice answer=d}
You sample 300 tokens from a trained model at temperature 0.05. What do you typically get?

- The most fluent text the model can produce.
- Random tokens.
- An error, because the logits overflow.
- A short phrase repeated over and over.

:::reveal
Near-zero temperature is greedy decoding: always the single most likely token. Once the model's most likely continuation leads back to a context it has seen, it loops. High temperatures fail the other way, sampling unlikely tokens until the text dissolves. Exercise 12 measures both with distinct n-gram ratios.
:::
::::

:::exercise{ref=e12}
:::

## What to take away

- Test every tokenizer on empty strings, runs of whitespace, newlines and non-ASCII text, and decide on a Unicode normalization before training.
- Report losses in bits per character when tokenizers differ.
- Sample with a temperature below 1 and top-p for readable text; greedy decoding repeats.
