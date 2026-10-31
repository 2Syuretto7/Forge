# Scale it: pipelines, checkpointing and real plans

## Pipelines

::::predict{id=p3 kind=numeric answer=0.4286 tol=0.01}
A model is split into 4 pipeline stages and each step streams 4 micro-batches. What fraction of the step is the bubble?

:::reveal
$(p - 1)/(m + p - 1) = 3/7 \approx 0.43$: almost half the time idle. With 32 micro-batches it falls to $3/35 \approx 0.09$, which is why pipelines need many micro-batches per step, and why the global batch limits how deep a pipeline can usefully be.
:::
::::

:::exercise{ref=e08}
:::

## Recomputation

:::exercise{ref=e09}
:::

## Planning

Try your plans in the planner: a 13B model on 64 GPUs, then a 175B model.

:::widget{name=ParallelismPlanner model=b13 dp=6}
:::

:::exercise{ref=e10}
:::
