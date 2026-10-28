# Capstone: a pretraining run that survives its own failures

Open the Colab notebook with a **T4 GPU** runtime (mount Google Drive first if you want checkpoints to survive a disconnection) and work through it:

1. Write `lr_at`, the warmup and cosine schedule as a function of the step.
2. Write `save_checkpoint` and `load_checkpoint`: every piece of state the next step depends on, written atomically. The notebook checks bitwise exact resume on a tiny model.
3. Write `evaluate`: the validation loss over fixed windows with a bootstrap interval.
4. Write `is_spike`, the trailing-window check the loop uses to roll back and skip data.
5. Run the 5,000-step training run, with corrupted data injected at position 3,000.
6. Write a report of at least 80 words: the configuration, the final validation loss with its interval, the spike and the recovery, and what you would monitor in a longer run.

The autograder checks the schedule, exact resume, the checkpoint contents, that the corruption was flagged within two batches and rolled back to an earlier checkpoint, that the step log is complete and never trained on corrupted data, a final validation loss below **1.70** nats per character that improved on the pre-spike value, and the report.
