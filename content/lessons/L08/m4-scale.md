# Scale and measure: memory and tooling

An engine that works is the start. Two measurements matter at scale: how much memory the tape holds, and how to switch recording off when you do not need gradients. A third tool, an automatic gradient checker for your own operations, makes the engine trustworthy.

:::exercise{ref=e10}
:::

::::predict{id=p4 kind=numeric answer=2.5 tol=0.3}
An MLP $512 \to 512 \to 512 \to 10$ processes one example. With recording on, the engine saves the input of each of the three linear layers and of each of the two ReLUs, all 512 values wide. Without recording, at most two 512-wide activations are alive at once. What is the ratio of saved values to the values alive in inference?

:::reveal
Saved: $5 \times 512 = 2560$ values; inference: $2 \times 512 = 1024$. The ratio is $2.5$. For deep networks the ratio grows with depth, because inference never needs more than a couple of layers at once while training keeps every layer's saved inputs until backward reaches them.
:::
::::

:::exercise{ref=e13}
:::

:::exercise{ref=e12}
:::
