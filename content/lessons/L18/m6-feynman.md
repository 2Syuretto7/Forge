# Explain it plainly: training a model too big for one GPU

Explain to a software engineer why a large model cannot be trained on one GPU and the main ways of splitting the work across many.

- Write 150 to 400 words.
- Account for where the memory goes.
- Explain data parallelism, ZeRO sharding, tensor parallelism and pipeline parallelism, each in a sentence or two, with its main cost.
- Mention one thing that makes a distributed job hang.

:::feynman{id=f1 prompt="Explain why large models cannot be trained on one GPU and how data parallelism, ZeRO sharding, tensor parallelism and pipeline parallelism split the work, including the main cost of each." key_points="Mixed-precision Adam needs about 16 bytes per parameter of model states, plus activations that grow with batch, sequence length and depth|Data parallelism splits the batch and averages gradients with an all-reduce, but keeps a full copy of the model on every GPU|ZeRO shards optimizer states, gradients and weights across the data-parallel GPUs, trading memory for extra gathers|Tensor parallelism splits weight matrices across GPUs with all-reduces inside every layer, so it needs fast links within a server|Pipeline parallelism splits the layers into stages and streams micro-batches, paying an idle bubble while the pipeline fills and drains|Every GPU must call the same collectives in the same order, or the job hangs"}
:::
