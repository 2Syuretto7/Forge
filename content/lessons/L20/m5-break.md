# Break it: the wrong loss and the wrong rank

## Training on the prompt

:::exercise{ref=e11}
:::

## Too few directions

::::predict{id=p4 kind=choice answer=a}
A LoRA fine-tune with rank 1 plateaus at a training loss well above full fine-tuning's, while rank 16 matches it. What is the best explanation?

- The update the task needs has more than one important direction, and a rank-1 adapter can only represent one.
- Rank 1 needs a larger learning rate, and nothing else.
- Rank 1 overfits.
- The adapter was initialized wrongly.

:::reveal
A rank-$r$ adapter can only produce rank-$r$ updates; by Eckart-Young its best possible loss is set by the singular values it cannot reach. More steps cannot fix that. Raise the rank, or adapt more matrices, and compare against full fine-tuning to see how much is left.
:::
::::

:::exercise{ref=e12}
:::

## What to take away

- Mask the prompt; include the end token in the response.
- Measure the base evaluation before and after every fine-tune.
- Start LoRA at rank 8 or 16 on all the large matrices, and check against full fine-tuning once.
- Distill with softened targets, and store only the teacher's top probabilities.
