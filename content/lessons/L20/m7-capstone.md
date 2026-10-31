# Capstone: from a raw crawl to a served model

One notebook runs the pipeline your design document planned, on one T4 in roughly 10 to 20 minutes:

1. **Clean** the noisy crawl of L12 (boilerplate, exact and near duplicates, junk, leaked validation text).
2. **Pretrain** a byte-level GPT on what survives, with mixed precision, the best checkpoint kept by validation loss, and checkpoints on Google Drive so a disconnected session resumes.
3. **Fine-tune** it with LoRA to write words in capitals and backwards, and merge the adapters.
4. **Improve** reversal with RL against an exact verifier, with a KL penalty to the fine-tuned model.
5. **Evaluate** every stage on test words fixed before training, greedy and sampled, with bootstrap intervals, and compare RL with fine-tuning item by item.
6. **Serve** the final model with the key-value cache and continuous batching, checking every answer against full recomputation.

The tools of L12 to L19 are provided, solved. You write the decisions and the glue: the plan within the compute budget, the order of the cleaning steps, the evaluation of a stage, the reward, the manifest that ties every stage's output to its input and configuration, and a final report of at least 200 words.

The autograder checks the budget, that no leaked or junk document survives cleaning, the manifest chain, the evaluation's shape, that the pretrained model reaches a validation loss below **1.9** nats per byte, that fine-tuning reaches **80%** greedy accuracy on capitals without raising the validation loss by 0.1, that RL raises sampled reversal accuracy with a paired interval above zero, that serving matches recomputation with a 95th-percentile inter-token latency under **50 ms**, and the report.

:::exercise{ref=capstone}
:::

:::colab{notebook=L20}
:::

## When you finish

You have taken a model through every stage, from raw text to answers served on demand, and you can defend each decision with a number. That is the whole path of this curriculum. Revisit the map: every node you have finished is a tool you have used.
