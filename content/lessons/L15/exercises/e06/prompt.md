# Exact resume

A run's state is more than its weights: Adam's moments and step count, and the random generator that draws the data. `batch(rng)` draws a regression batch.

1. `loss_grad(w, X, y)`: $\tfrac12 \operatorname{mean}((Xw - y)^2)$ and its gradient.
2. `new_state(seed)` and `train_steps(state, n, lr=0.05)`: Adam steps on fresh batches from the state's generator.
3. `save(state)`: a checkpoint sharing nothing with the live state, including `rng.bit_generator.state`.
4. `load(ckpt)`: a live state from it.

Training 100 steps straight must give **bitwise** the same weights as training 40, saving, training a few more steps (which are then discarded), loading, and training 60.

## Hints

1. Copy arrays (`.copy()`) and the generator state (`copy.deepcopy`), or later steps will change the checkpoint.
2. Restoring the step count matters: Adam's bias correction uses it.
3. A run that restores everything but the data generator still "works", but it trains on different batches after every restart and cannot be reproduced.
