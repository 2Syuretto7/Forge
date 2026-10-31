# Training with minibatches

Train an MLP on the spiral with minibatch stochastic gradient descent.

- `sgd_step(params, grads, lr)`: update every parameter in place.
- `train(params, X, y, lr, epochs, batch, seed, act)`: each epoch, shuffle with `np.random.default_rng(seed + epoch).permutation(n)`, step through consecutive batches, and record the loss of every batch. Return the list of batch losses.

Use `loss_and_grads` from exercise 4 (copy it in). The test trains a `2 -> 100 -> 3` ReLU network and requires training accuracy above 95 percent.

## Hints

1. `for k in params: params[k] -= lr * grads[k]`.
2. Batches: `perm[i:i + batch]` for `i` in `range(0, n, batch)`.
3. A learning rate of about 1 works for this small, standardized problem.
