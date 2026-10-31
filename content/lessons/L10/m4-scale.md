# Scale and measure: sampling and losses

## Controlling generation

:::exercise{ref=e08}
:::

:::exercise{ref=e09}
:::

## Regularizing the target

:::exercise{ref=e10}
:::

::::predict{id=p4 kind=numeric answer=6.25 tol=0.1}
The capstone's tokenizer has a vocabulary of 512. What cross-entropy, in nats per token, does an untrained model have if it predicts uniformly?

:::reveal
$\ln 512 \approx 6.24$ nats per token. The capstone's first logged loss is close to that (a randomly initialized model with small embeddings predicts nearly uniformly), which is a useful check that the loss is computed correctly before training starts.
:::
::::
