# Break it: post-norm without warmup

The stack, Adam and your `train` are provided.

1. `dead_fraction(p, X, depth, mode)`: for each hidden layer, the fraction of its ReLU units whose pre-activation is not positive for any row of `X`.
2. `warmup_experiment(lr=1e-2, warmup=150, depth=20, width=32, steps=300, seed=0)`: train the post-norm stack without warmup and with it. For each run return `(loss, dead_top)`: the mean of the last 30 minibatch losses, and the mean dead fraction over the top third of the layers on `make_digits(500, 1)`. Return `{"none": ..., "warmup": ...}`.

Each run takes under a second natively and a few seconds in the browser.

## Hints

1. Recompute the forward pass of `mode` layer by layer, recording `(z > 0).sum(axis=0) == 0` per unit.
2. The top third is `dead[2 * depth // 3:]`.
3. Same seed for both runs, so warmup is the only difference.
