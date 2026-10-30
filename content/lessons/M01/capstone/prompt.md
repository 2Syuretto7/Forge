# Capstone: a Fermi pack of twelve estimates

The starter defines the facts behind twelve ML-flavoured quantities: an MLP's shape, an embedding table, a training run, a GPU, an image dataset, attention shapes and a text corpus. Do three things, in this order.

**1. Estimate.** Fill in `ESTIMATES`: for each of the twelve names, an interval `(lo, hi)` of what you believe, written before you compute anything. Each interval must satisfy `0 < lo < hi` and be no wider than a factor of 30 from end to end (`hi / lo <= 30`).

| Name | Quantity |
| --- | --- |
| `mlp_flops` | FLOPs of one forward pass of the MLP with widths 784, 512, 512, 10 on a batch of 64 |
| `mlp_params` | weights plus biases of that MLP |
| `embedding_bytes` | bytes of a float32 embedding table for 50,000 tokens of 768 dimensions |
| `adam_gb` | GB (of $10^9$ bytes) to train 1.3 billion parameters with Adam at 16 bytes each |
| `train_flops` | $6ND$ for 125 million parameters on 2.5 billion tokens |
| `gpu_hours` | GPU-hours for that run at $10^{14}$ FLOP/s and 40 percent utilization |
| `run_cost` | dollars for those GPU-hours at 2 dollars per hour |
| `imagenet_bytes` | bytes of 1,281,167 images of $224 \times 224$ pixels with 3 one-byte colour channels |
| `steps_per_epoch` | optimizer steps to pass once over those images in batches of 256 (a last partial batch counts) |
| `attention_entries` | entries of the attention score matrices for sequences of 2,048 tokens, 12 heads and a batch of 8 (one score per pair of positions per head) |
| `corpus_words` | words in `CORPUS`: 3,000 sentences of 8 to 20 words |
| `corpus_chars` | characters in `CORPUS`, spaces and full stops included; words have 2 to 9 letters |

**2. Compute.** Write `truths()`, returning a dictionary with the exact value of each quantity, computed from the constants in the starter (for the corpus, count it).

**3. Score.** Write `score(estimates, truths)`: the number of quantities whose true value is within a factor of 3 of the geometric midpoint $\sqrt{\text{lo} \cdot \text{hi}}$ of its interval.

The tests check every true value and require a score of at least 10 out of 12.
