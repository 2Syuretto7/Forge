# A training loop with an optimizer and a schedule

Your optimizers from exercise 8 and the L03 network are provided. Implement `train(opt, X, y, steps, batch=50, schedule=None, seed=0, sizes=(64, 64, 32, 10))`:

- initialize with `init(list(sizes), seed)` and create `rng = np.random.default_rng(seed)`;
- each epoch draws `perm = rng.permutation(n)` and visits it in consecutive full batches of size `batch` (drop the remainder), starting a new epoch when one is exhausted, until `steps` steps have run;
- step `t` (counted from 1) calls `opt.step(params, grads, lr)` with `lr = schedule(t)` if a schedule is given, otherwise `None`;
- return `(params, losses)` with the minibatch loss of every step.

The tests also check that plain SGD at rate 0.3 for 600 steps reaches at least 88 percent test accuracy.

## Hints

1. A `while t < steps` loop around a `for i in range(0, n - batch + 1, batch)` loop, breaking out when `t` reaches `steps`.
2. `idx = perm[i:i + batch]`, then `loss_and_grads(params, X[idx], y[idx])`.
3. Following this order exactly makes your runs reproducible against the tests.
