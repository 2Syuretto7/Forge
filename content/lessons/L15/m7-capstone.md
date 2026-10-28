# Capstone: predict a run before you train it

In the notebook you train twenty small character-level GPTs on Tiny Shakespeare: four layers at five widths, from 51 thousand to 790 thousand non-embedding parameters, each at four token budgets from half a million to four million characters. You fit $L(N, D) = E + A N^{-\alpha} + B D^{-\beta}$ to them with the method of exercise 5, derive the compute-optimal frontier, and then write down the predicted loss of a model more than twice as large as any in the sweep **before** training it.

At this scale every run is still early in training, where the loss falls roughly linearly in the logarithm of the tokens, so the floor $E$ is not determined and the fit pins it at zero; the exponents describe this regime only. That is a finding, not a failure: it is exactly the situation in which extrapolating far beyond the sweep would mislead. The autograder checks that the fit describes the sweep (relative RMS error below 3%), that the prediction was recorded before the held-out run started, and that it lands within 8% of the measured loss.

:::exercise{ref=capstone}
:::

:::colab{notebook=L15}
:::

## When you finish

You can now size a training run from a budget and check the plan against small experiments. L18 asks what happens when the model you sized no longer fits on one GPU; L19 runs a real pretraining job and watches it for the failures that small sweeps never show.

:::edge{to=L18 text="When the model no longer fits on one GPU."}
:::

:::edge{to=L19 text="A real pretraining run, monitored and recovered."}
:::
