# Recall bridge: saved tensors, bytes and bandwidth

From L08: backward needs tensors saved during the forward pass. From L17: mixed-precision training keeps 16-bit weights and gradients next to fp32 master weights and Adam's two moments. From L11: moving bytes costs time, and overlapping transfers with compute hides it. From L15: the compute-optimal model for a large budget has billions of parameters. Put together, a model worth training does not fit on one GPU. Reviews due from L08, L11, L15 and L17 appear above.

::::derivation{id=d0 title="Warm-up"}
:::step
In mixed precision with Adam, each parameter costs $2 + 2 + 12 =$ [[16]] bytes of model state.
:::
:::step
A 7-billion-parameter model therefore needs [[112]] GB before any activations.
:::
:::step
The 16-bit weights of a 70-billion-parameter model alone take [[140]] GB.
:::
::::
