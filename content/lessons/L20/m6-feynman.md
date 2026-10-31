# The design document

Write the design document for the capstone pipeline, 400 to 1,500 words, before running it. It is graded on correctness, completeness, justification (each decision cites a measurement, a calculation or an earlier lesson), tradeoffs (the main alternative for each decision and what would change it), and clarity (a reviewer could reproduce the plan from it).

- Data: the cleaning steps, their order and thresholds, decontamination, and how you will show the cleaning helped.
- Model and budget: size, context, steps and batch, defended against the data and the compute.
- Training: optimizer, schedule, precision, checkpoints and spike handling.
- Fine-tuning and RL: method, hyperparameters, forgetting margin, reward and KL weight.
- Evaluation: held-out sets, intervals, paired comparisons, number of items.
- Serving: targets, workload, and the correctness check.

:::feynman{id=f1 rubric=design prompt="Write the design document for a pipeline that cleans a small crawl, pretrains a byte-level GPT on one T4, fine-tunes it with LoRA, improves it with RL on an exact-match reward, evaluates every stage, and serves it, defending each choice." key_points="The data plan orders boilerplate removal, exact and near deduplication, quality rules and decontamination against every evaluation set, and tests the cleaning with equal-compute training runs|The model size is defended against the data budget, recognizing that about a million training tokens makes the run data-limited so it uses many epochs with regularization and validation-based checkpoint selection instead of the Chinchilla ratio|The training recipe names the optimizer, warmup and cosine schedule, clipping, checkpoints with full state for exact resume, and a spike check with rollback|Fine-tuning masks the prompt, trains LoRA adapters with a stated rank and learning rate, and limits forgetting measured as base loss on held-out text|RL uses an exact-match reward with group-relative advantages and a KL penalty to the fine-tuned model, with a check for reward hacking|Every stage is evaluated on held-out items fixed before training, with bootstrap intervals and paired comparisons, and enough items to resolve the expected differences|Serving uses a key-value cache and continuous batching with stated latency and throughput targets and a check against full recomputation"}
:::
