# Capstone: from a raw crawl to a served model

Open the Colab notebook with a **T4 GPU** runtime, mount Google Drive if you want the pretraining checkpoint to survive a disconnection, and work through it:

1. Write `PLAN` from your design document: the pretraining run within the compute budget, then the LoRA and RL settings.
2. Write `clean_crawl` from the provided L16 functions, in the right order.
3. Write `record` and `check_chain`, the manifest that links every stage's output to its input and configuration.
4. Run pretraining (resumable from Drive) and fine-tuning.
5. Write `evaluate_stage`: validation loss, and greedy and sampled accuracy per test word for each task.
6. Write `rl_reward` and run RL on reversal; compare with fine-tuning item by item.
7. Serve the final model and check its answers against recomputation.
8. Write a final report of at least 200 words: every stage's result with its interval, what surprised you, and what you would do with ten times the compute.

The autograder checks the budget, the cleaning, the manifest chain, the evaluation, a validation loss below **1.9**, at least **80%** greedy accuracy on capitals after fine-tuning with less than 0.1 rise in validation loss, a positive paired gain from RL in sampled reversal accuracy, serving that matches recomputation with a 95th-percentile inter-token latency under **50 ms**, and the report.
