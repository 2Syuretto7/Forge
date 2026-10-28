# Break it: too few items

Implement `compare_models(acc_a, acc_b, n_items, seed=0, n_boot=2000)`: simulate two models with true accuracies `acc_a` and `acc_b` answering `n_items` items independently, and return the paired bootstrap interval of their accuracy difference.

With 20 items a ten-point gap is indistinguishable from noise; with 2,000 it is clear.

## Hints

1. Draw both models' answers from one generator, model A first.
2. Use the paired bootstrap of exercise 2.
3. Before trusting a comparison, check the interval of the difference excludes zero.
