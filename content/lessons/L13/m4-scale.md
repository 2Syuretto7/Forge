# Scale and measure: memory and speed

:::exercise{ref=e09}
:::

::::predict{id=p4 kind=numeric answer=112 tol=2}
How many gigabytes of weights, gradients and Adam state does training a 7-billion-parameter model need in mixed precision, before any activations?

:::reveal
$7 \times 10^9 \times 16$ bytes $= 112$ GB: more than an 80 GB GPU holds, before a single activation is stored. Mixed precision does not shrink this; L14 shows how to split it across GPUs.
:::
::::

:::exercise{ref=e10}
:::
