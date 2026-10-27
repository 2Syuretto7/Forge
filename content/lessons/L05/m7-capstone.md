# Capstone: a calibrated multi-class classifier

You receive a tabular dataset with eight features on wildly different scales and three classes. Build the full pipeline: split, standardize, train a regularized softmax classifier, evaluate it on held-out data, and analyze its calibration. The target is at least 87 percent test accuracy with a calibration error below 0.06.

:::exercise{ref=capstone}
:::

## When you finish

You now have a complete, honest supervised learning pipeline. Every later model reuses it with a more expressive function in place of $XW + b$: L07 replaces it with a multi-layer network trained by backpropagation, L13 with a transformer. The loss, the gradient $P - Y$ at the output, the standardization, the held-out evaluation and the calibration check all stay.

:::edge{to=L07 text="Replace the linear score with a learned multi-layer function and keep everything else."}
:::

:::edge{to=L06 text="Why does held-out error behave the way it does? Bias, variance and double descent."}
:::
