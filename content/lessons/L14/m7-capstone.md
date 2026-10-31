# Capstone: plan a run, then simulate it

The notebook has two parts, and runs on any Colab runtime (CPU is enough).

**The plan.** A 13-billion-parameter model (40 layers, width 5120, 40 heads) is to be trained with sequence length 2048 on 64 GPUs of 80 GB in 8 servers. You choose the degrees of tensor, pipeline and data parallelism, the ZeRO stage, the micro-batch and checkpointing, check the memory per GPU with the planner's formulas, and justify the choice in writing.

**The simulation.** Four CPU processes talk through `torch.distributed` with the gloo backend. You write gradient averaging for data parallelism, ZeRO stage 1 with a reduce-scatter and an all-gather, and a tensor-parallel MLP, and check each against a single-process reference. A last section measures the bytes saved for backward with and without `torch.utils.checkpoint`.

:::exercise{ref=capstone}
:::

:::colab{notebook=L14 runtime=cpu}
:::

## When you finish

You can plan the hardware for a run and implement the communication it needs. L15 runs a real pretraining job and handles what goes wrong during one: spikes, crashes and resumption.

:::edge{to=L15 text="A real pretraining run, monitored and resumable."}
:::
