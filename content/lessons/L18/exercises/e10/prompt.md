# Planning for real model sizes

`memory_per_gpu(m, tp, pp, dp, zero, checkpoint)` is the planner's formula (model states of one shard under ZeRO, plus the first stage's activations with FlashAttention, sequence 2048 and micro-batch 1). `MODELS` has three real shapes.

Implement `find_plan(model, n_gpus, gpu_bytes, node_size=8)`: search $t \in \{1, 2, 4, 8\}$ (at most `node_size`, so tensor parallelism stays inside a node), $p \in \{1, 2, 4, 8, 16\}$ dividing the layer count, $d = n_\text{gpus}/(tp)$ when whole, ZeRO stages 0 to 3 and checkpointing off or on. Keep plans using at most 90% of `gpu_bytes`. Prefer the smallest $t \cdot p$, then the smallest $t$, then the lowest ZeRO stage, then no checkpointing. Return a dictionary with `tp, pp, dp, zero, checkpoint, bytes`, or `None`.

## Hints

1. A tuple `(tp * pp, tp, zero, checkpoint)` sorts in the order of preference (`False < True`).
2. The preference encodes cost: model parallelism adds communication inside every layer, higher ZeRO stages add all-gathers, checkpointing adds a forward pass.
3. The 10% margin covers what the formula leaves out: logits, temporary buffers, fragmentation.
