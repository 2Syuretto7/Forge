# Build: a tokenizer and a language-modeling pipeline

## Bytes and merges

:::exercise{ref=e01}
:::

:::exercise{ref=e02}
:::

:::exercise{ref=e03}
:::

:::exercise{ref=e04}
:::

## Data and baselines

:::exercise{ref=e05}
:::

:::exercise{ref=e06}
:::

::::predict{id=p3 kind=choice answer=a}
A bigram model with add-one smoothing is trained on the training split and evaluated on validation text. Compared with its training loss, its validation loss is:

- Higher, and the gap grows with the vocabulary size, because more bigrams are never seen in training.
- Lower, because smoothing helps.
- Equal, because a bigram model cannot overfit.
- Infinite, because some validation bigrams never occur in training.

:::reveal
Smoothing keeps every probability positive, so the loss is finite, but bigrams that never appeared in training get only the smoothed share, and with $V^2$ possible pairs a larger vocabulary leaves more of them unseen. This is overfitting in its simplest form, and the reason language models are always evaluated on held-out text.
:::
::::

:::exercise{ref=e07}
:::
