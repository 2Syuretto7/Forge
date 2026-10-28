# The design document

A design document states what you will build, how, and why each choice beats its alternatives, before you spend the compute. Yours covers the six stages of the capstone. For each decision, give the alternative you considered, the evidence (a measurement from an earlier lesson, a paper, or a calculation), and what result would change your mind. The sections below set out the decisions and the arithmetic; the document itself, 400 to 1,500 words, is written in movement 6 and graded with a design rubric: correctness, completeness, justification, tradeoffs and clarity.

## 1. Data

The capstone starts from the noisy crawl of L16: exact and near duplicates, boilerplate, junk pages, and leaked validation text. Decide the order of the cleaning steps (boilerplate before exact deduplication, so pages that differ only by a footer collapse), the thresholds of the quality rules and of MinHash, and how you will show the cleaned data is better: a model trained on each at equal compute, scored on text that never leaked. Decontaminate against every evaluation set you will use later, including the fine-tuning test words.

::::derivation{id=d1 title="How much data"}
:::step
Tiny Shakespeare has 1,115,394 bytes. With 90% for training, the training split has about [[1.004e6|tol=1e3]] bytes.
:::
::::

:::edge{from=L19 text="the pretraining run"}
:::

## 2. Model and budget

Choose the architecture (the decoder of L13 and L14 with pre-norm residual blocks, L10), the width, depth and context, and the number of steps and batch size. Defend the size against the data, not just the compute: with about a million training tokens the run is data-limited (puzzle 1), so you will train for many epochs with dropout and choose the final checkpoint by validation loss.

::::derivation{id=d2 title="The pretraining budget"}
:::step
3,000 steps of 32 windows of 256 tokens is [[24576000]] tokens.
:::
:::step
That is about [[24.5|tol=0.1]] passes over the training split.
:::
:::step
At $6ND$ with $N = 10.7$ million, the run costs about [[1.58e15|tol=1e13]] operations, roughly 11 minutes at 2.4 TFLOP/s.
:::
::::

## 3. Training that survives

Name the recipe and why: AdamW with warmup and cosine decay (L09), gradient clipping, mixed precision where the hardware supports it (L17), checkpoints with every piece of state and a deterministic data order so a disconnected Colab session resumes exactly, and the spike check with rollback of L19. State what you will log and what would make you stop the run.

## 4. Fine-tuning and RL

Fine-tuning teaches the instruction format and the tasks (L20): the prompt is masked out of the loss, LoRA adapters train a small fraction of the parameters, and the base loss on ordinary text measures forgetting. Choose the rank, which layers get adapters, the learning rate and the number of steps, and the forgetting margin you accept. RL then raises accuracy on a task with a verifiable reward (L21): exact match on the answer. Choose the group size for group-relative advantages, the KL weight and the number of updates, and say how you will detect reward hacking.

:::edge{from=L20 text="LoRA fine-tuning"}
:::

:::edge{from=L21 text="RL with a verifiable reward"}
:::

## 5. Evaluation

Every reported number gets an interval over items (L23). Decide the held-out sets: test words never seen in fine-tuning or RL, chosen before training and checked for overlap. Decide the comparisons: base against fine-tuned against RL, paired by item. Decide how many items you need to resolve the differences you expect.

::::derivation{id=d3 title="Enough items"}
:::step
To measure an accuracy near 50% to within $\pm 5$ points at 95% confidence, $1.96^2 \cdot 0.25 / 0.05^2$ rounds up to [[385]] items.
:::
::::

:::edge{from=L23 text="intervals over items"}
:::

## 6. Serving

Serve the final model with the key-value cache and continuous batching of L22, state the latency and throughput targets and the workload you will test them with, and check that served outputs match full recomputation.

::::derivation{id=d4 title="The cache"}
:::step
In float32 the 6-layer, width-384 model caches $2 \times 6 \times 384 \times 4 =$ [[18432]] bytes per token.
:::
:::step
32 sequences of 256 tokens take about [[151|tol=1]] MB, a tiny fraction of a T4's 16 GB: this server is limited by per-step overhead, not memory.
:::
::::

:::edge{from=L22 text="the inference server"}
:::

## 7. Reproducibility and the report

Record a manifest: for each stage, a digest of its input, its configuration and its output (exercise 10), so every number in the report traces to the data and settings that produced it. The final report gives each stage's result with its interval, what went wrong, and what you would do with ten times the compute.
