# Size the run from the budget

The capstone has one T4 for about an hour of pretraining. Turn that into a plan (L15).

1. `compute_budget(peak_flops, utilization, hours)`: the operations available.
2. `chinchilla_split(C, tokens_per_param=20)`: $N$ and $D$ with $C = 6ND$ and $D = 20N$.
3. `epochs(D, corpus_tokens)`: how many passes over the corpus that takes.

## Hints

1. $C = 6 \cdot 20 N^2$, so $N = \sqrt{C/120}$.
2. A T4 peaks at about 65 TFLOP/s in 16-bit; small models in eager PyTorch reach well under half of that.
3. If the compute-optimal plan needs hundreds of epochs, the run is limited by data, not compute: choose a smaller model and repeat the data only a few times.
