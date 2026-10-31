# Scale and measure: training at depth

Statistics at initialization predict trouble; training confirms it. These exercises train 20- and 30-layer stacks on the L03 digits with Adam.

::::predict{id=p4 kind=choice answer=a}
Train a 20-layer residual stack without normalization, with He-initialized branches, using Adam for 300 steps. What happens?

- It barely trains: the forward pass is already enormous at initialization.
- It trains as well as the pre-norm stack, because the skip connections carry the gradient.
- It trains slowly but steadily.
- It trains better than the pre-norm stack, because there is no normalization to slow it down.

:::reveal
At initialization the stream is about 20,000 times larger at the top than at the bottom, the logits are enormous, and the loss starts near 30,000; after 300 Adam steps it is still above 3, worse than guessing uniformly ($\ln 10 \approx 2.3$). Scaling every branch by $1/\sqrt{20}$, with no normalization at all, is enough to make the same network train: exercise 9.
:::
::::

:::exercise{ref=e08}
:::

:::exercise{ref=e09}
:::

## Batch statistics

:::exercise{ref=e10}
:::
