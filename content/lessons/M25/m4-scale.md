# Scale: 100,000 examples and the coverage of intervals

A model scores 83 percent on 100,000 test examples. How precise is that number, and is the next model, at 84 percent, really better? The bootstrap answers both, if you can afford it.

::::predict{id=p4 kind=choice answer=d}
A bootstrap of 100,000 examples with 2,000 resamples, done by drawing index arrays, needs how much memory for the indices alone?

- About 1.6 MB
- About 16 MB
- About 160 MB
- About 1.6 GB

:::reveal
About 1.6 GB: $2 \times 10^8$ integers of 8 bytes. But the mean of a resample depends only on how many times each distinct value was drawn, and for 0/1 scores that is one binomial count per resample: 2,000 numbers instead of 200 million.
:::
::::

:::exercise{ref=e13}
:::

:::exercise{ref=e12}
:::
