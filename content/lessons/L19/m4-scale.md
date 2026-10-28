# Scale it: finding causes and recovering

## Which examples?

:::exercise{ref=e08}
:::

## Rolling back

::::predict{id=p3 kind=numeric answer=54 tol=2}
Writing a checkpoint of a large model takes one minute, and the cluster loses a node about once a day. Using the Young/Daly rule, roughly how many minutes apart should checkpoints be?

:::reveal
$T^* = \sqrt{2 C M} = \sqrt{2 \cdot 60 \cdot 86400} \approx 3220$ seconds, about 54 minutes. Checkpointing more often wastes time writing; less often loses more work at each failure. As clusters grow, $M$ shrinks and checkpoints must get faster, which is why large runs save them asynchronously and shard them across nodes.
:::
::::

:::exercise{ref=e09}
:::

## Watching every layer

:::exercise{ref=e10}
:::
