# Capstone: plan a run, then simulate it

Open the Colab notebook; the default CPU runtime is enough.

1. Choose `PLAN` for a 13-billion-parameter model on 64 GPUs of 80 GB: tensor, pipeline and data-parallel degrees, ZeRO stage, micro-batch size and checkpointing. The notebook computes the memory per GPU and the pipeline bubble.
2. Write `ring_reduce_scatter` and `ring_all_gather` with `dist.isend` and `dist.recv` between four processes.
3. Write `average_gradients` for data parallelism.
4. Write `zero1_worker`: Adam on each rank's slice of the parameters, with your ring collectives.
5. Write the two autograd functions of a tensor-parallel MLP.
6. Write `saved_bytes` and compare the memory saved for backward with and without checkpointing.
7. Write a report of at least 80 words justifying the plan.

The autograder checks that the plan is valid, fits in **90% of the GPU** with a bubble below **10%**, that your ring collectives equal `dist.all_reduce`, that data parallelism and ZeRO-1 match single-process SGD and Adam, that each ZeRO rank stores a quarter of the optimizer state, that the tensor-parallel MLP matches the dense one in forward and backward, that checkpointing cuts saved memory below a quarter, and the report.
