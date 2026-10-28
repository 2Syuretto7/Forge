# Break it: batches of one and post-norm without warmup

## A batch of one

::::predict{id=p5 kind=choice answer=c}
A model trained with batch norm is fine-tuned with a batch size of 1, still in training mode. What does each batch-norm layer output, and what gradient does it pass back?

- Its input unchanged, and the upstream gradient unchanged.
- Random values, and a random gradient.
- $\beta$, whatever the input, and a gradient of zero.
- An error, because the variance is zero.

:::reveal
With one example, the batch mean is the example itself and the variance is zero, so $\hat x = 0 / \sqrt{\epsilon} = 0$ for every feature and the output is $\beta$. The backward formula gives $N g - \sum g - \hat x \sum g \hat x = g - g - 0 = 0$: nothing below the layer can learn. Use evaluation mode (running statistics) or a normalization that does not depend on the batch.
:::
::::

:::exercise{ref=e11}
:::

## Post-norm without warmup

The post-norm stack from Movement 3, at depth 30 and width 32, trained with Adam at a rate of 0.007 for 300 steps: without warmup the loss ends near 2.2 in this lesson's reference run, with a 150-step warmup near 1.6, and the pre-norm stack at the same depth reaches about 0.3 even at a rate of 0.01 with no warmup. Across three seeds warmup helped post-norm every time, by between 0.2 and 0.6 in final loss. In two of the three seeds, about a tenth of the ReLU units in the top layers were dead after the run without warmup, against one or two percent with it: large early steps push units into a region they never leave.

:::exercise{ref=e12}
:::

## What to take away

- Batch norm couples the examples in a batch; never train it with tiny batches, and switch to evaluation mode for inference.
- Prefer pre-norm residual blocks with a final norm; if you must use post-norm, warm the learning rate up.
- Check the scale of activations and gradients per layer at initialization before training anything deep.
