# Learning-rate sweeps

Before comparing optimizers, find each one's best learning rate. Implement:

1. `sweep(make_opt, lrs, X, y, steps=300, seed=0)`: for each rate, train with `make_opt(lr)` (your `train` from exercise 10 is provided) and record the final training loss on the full data set with `full_loss`; record `inf` for a run whose loss is not finite or exceeds 10.
2. `best_lr(lrs, losses)`: the rate with the lowest loss.

Then sweep SGD over $10^{-3}$ to $10^{0.5}$ and Adam over $10^{-4}$ to $10^{-0.5}$ in half-decade steps, and compare the shapes of the two curves with your sketch.

## Hints

1. Wrap the training in `with np.errstate(all="ignore"):` so overflowing runs do not flood the output with warnings.
2. `np.isfinite(v) and v <= 10` decides whether a run survived.
3. Look at the SGD runs at rates 2 and 3: the loss does not explode, it gets stuck near $\ln 10$. Count the ReLU units of the second layer that never fire.
