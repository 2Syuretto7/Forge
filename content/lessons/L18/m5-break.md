# Break it: silent cache bugs and outliers

## A wrong position

::::predict{id=p4 kind=choice answer=c}
A cached generator gives each new token the position embedding of the token before it. What do you see?

- An index error on the first generated token.
- Identical output, since positions are approximate anyway.
- Plausible output that differs from what the model would produce without the cache, noticed only by comparing the two.
- Output that is all one repeated token.

:::reveal
Nothing crashes: the shapes are right and the text is fluent enough. The model is simply running on slightly wrong inputs. Comparing cached generation with full recomputation, token by token, finds the first divergence (exercise 11); run that comparison on every change to an inference engine.
:::
::::

:::exercise{ref=e11}
:::

## Outliers

:::exercise{ref=e12}
:::

## What to take away

- Decode is memory-bound: batch requests, shrink the weights, and keep the caches small.
- Test every cache, batching or quantization change against unoptimized generation.
- Quantize per row or per group, calibrate on real activations, and keep outlier features in high precision.
- Speculative decoding speeds up generation without changing its distribution; it pays when the draft agrees often and costs little.
