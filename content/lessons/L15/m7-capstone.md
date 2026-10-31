# Capstone: a pretraining run that survives its own failures

You write the pieces of a real training script (the schedule, atomic checkpoints with every piece of state, the spike check, and an evaluation harness with bootstrap intervals), check exact resume on a tiny model, and run the nanoGPT-sized character model (6 layers, width 384, 10.7 million parameters) for 5,000 steps on Tiny Shakespeare. At data position 3,000 the stream turns into random characters for ten batches; your detector must catch it, restore the checkpoint from before, skip the data and continue. On a T4 the run takes roughly 15 to 25 minutes: Tiny Shakespeare supports no longer run without overfitting. The same script runs for hours on a larger corpus, and with checkpoints on Google Drive it resumes after a disconnected session.

The autograder checks the schedule, bitwise exact resume, the checkpoint contents, that the spike was flagged within two batches of the corruption and rolled back to a checkpoint before it, that the logged steps are complete and contain no corrupted data, a final validation loss below **1.70** that is lower than before the spike, and the report.

:::exercise{ref=capstone}
:::

:::colab{notebook=L15}
:::

## When you finish

You have run a pretraining job the way large ones are run, at small scale. L16 starts from a pretrained model and adapts it with fine-tuning; L20 runs the whole pipeline end to end.

:::edge{to=L16 text="Fine-tuning the pretrained model."}
:::
