# Break it: leaks between stages and skew at the end

## Evaluating on what you trained on

::::predict{id=p4 kind=choice answer=b}
The fine-tuning set and the evaluation set were sampled from the same list of words, with replacement. Fine-tuned accuracy is 92%. What is the likely problem?

- None: sampling with replacement is the standard way to build both sets.
- Some evaluation words were also trained on, so 92% mixes memory with generalization; the accuracy on words never trained on may be much lower.
- The evaluation set is too large.
- The model overfits, so the true accuracy is higher.

:::reveal
Any overlap between training and evaluation inflates the score on exactly the overlapping items (L16, L23). Split the word list once, before any training, and check the overlap explicitly (exercise 11). Report the clean accuracy.
:::
::::

:::exercise{ref=e11}
:::

## Train/serve skew

:::exercise{ref=e12}
:::

## What to take away

- Plan from the binding constraint: on a small corpus, data, not compute.
- Fix the evaluation sets before training and check every stage's data against them.
- Measure each stage against the one before, paired by item, with intervals.
- Record what each stage read and wrote, and share one encoder between training and serving.
