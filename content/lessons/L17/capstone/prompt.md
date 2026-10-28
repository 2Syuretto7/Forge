# Capstone: the GPT in mixed precision

Open the Colab notebook with a **T4 GPU** runtime and work through it:

1. Write `format_info(dtype)` from `torch.finfo`: bits, epsilon, largest value and smallest normal value.
2. Write `train_amp(model)`: the provided fp32 training loop with the forward pass and loss under `torch.autocast` and, for fp16, a `torch.amp.GradScaler` (scale the loss before `backward`, unscale before gradient clipping, step and update through the scaler).
3. Run both trainings from the same initial weights and write a report of at least 80 words on the formats, the measured speedup and memory, the agreement of the losses and the scaler's role.

The autograder checks the format table, that the final losses agree within 3 percent and that training made progress, and, on the GPU, a speedup of at least 1.5 and lower peak memory.
