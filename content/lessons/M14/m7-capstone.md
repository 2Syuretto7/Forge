# Capstone: a PCA pipeline for an embedding set

The starter generates 1,500 points in 48 dimensions, in six named groups of eight features. Build the full PCA pipeline, find how many components reach 95 percent of the variance, check the reconstruction error against Eckart-Young, and write what the top three components measure.

:::exercise{ref=capstone}
:::

## When you finish

You can find the important directions of any dataset and say how much you lose by keeping only those. M23 adds the probability behind covariance matrices; M33 computes the top singular vectors of matrices too large for a full SVD; M34 explains why random directions in 768 dimensions are almost perpendicular, which is why a few strong directions stand out so clearly.

:::edge{to=M33 text="randomized SVD finds the top singular vectors from a few matrix products."}
:::

:::edge{to=M34 text="in high dimension random directions are nearly perpendicular, so real structure stands out in the spectrum."}
:::
