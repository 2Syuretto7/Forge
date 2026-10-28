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

Take the post-norm stack from Movement 3 at depth 20 and width 32, and train it with Adam at a rate of 0.01 for 300 steps. In this lesson's reference runs (seeds 0, 1 and 2), the final loss without warmup was 1.47, 2.31 and 1.99; with a 150-step linear warmup, 0.95, 0.89 and 0.83. The pre-norm stack at the same depth and rate, with no warmup, reached 0.24, 0.22 and 0.28. Without warmup, between 5 and 65 percent of the ReLU units in the top third of the post-norm stack were dead after training, against at most half a percent with warmup: large early steps push units into a region they never leave. Your numbers in the browser will differ somewhat: its NumPy rounds differently, and 300 steps of training amplify tiny differences, but warmup still wins.

:::exercise{ref=e12}
:::

## What to take away

- Batch norm couples the examples in a batch; never train it with tiny batches, and switch to evaluation mode for inference.
- Prefer pre-norm residual blocks with a final norm; if you must use post-norm, warm the learning rate up.
- Check the scale of activations and gradients per layer at initialization before training anything deep.
