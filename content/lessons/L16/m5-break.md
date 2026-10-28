# Break it: leaked benchmarks and broken resumption

## A leaked test set

::::predict{id=p4 kind=choice answer=a}
A 4-gram model and a bigram model are trained on a corpus that, unknown to you, contains the evaluation documents. The text comes from a process where only the previous word matters. Which looks better on the evaluation set?

- The 4-gram model, by a wide margin.
- The bigram model, because it matches the process.
- They look the same.
- Neither: the leak makes both scores infinite.

:::reveal
The 4-gram model memorizes the exact sequences it saw, including the leaked evaluation text, so its evaluation loss collapses. On fresh text the bigram model is better. Contamination does not just inflate a score; it can pick the wrong model. Exercise 11 measures both.
:::
::::

:::exercise{ref=e11}
:::

## A shuffle buffer that forgets

:::exercise{ref=e12}
:::

## What to take away

- Deduplicate exactly, then approximately, before anything else; strip boilerplate lines.
- Filter with simple rules first, and check what a classifier removes.
- Decontaminate the training set against every evaluation set, and report scores on clean examples.
- Save every piece of loader state in the checkpoint, and test resumption by comparing with an uninterrupted run.
