# Capstone: a 30-layer network that trains

Build and train a residual network with at least 30 hidden layers on the L07 digit task, with every gradient written by hand, and explain each choice that keeps it stable.

:::exercise{ref=capstone}
:::

## When you finish

You have built, in miniature, the backbone of every transformer: a pre-norm residual stream. L13 replaces the MLP branch with attention, and L12 turns the layer norm into a fused GPU kernel.

:::edge{to=L13 text="The residual stream becomes the transformer's backbone."}
:::
