import copy
import numpy as np

TRUE_W = np.array([1.0, -2.0, 0.5])


def batch(rng, n=16):
    """A regression batch drawn from the trainer's generator."""
    X = rng.normal(size=(n, 3))
    return X, X @ TRUE_W + 0.1 * rng.normal(size=n)


def loss_grad(w, X, y):
    r = X @ w - y
    return 0.5 * np.mean(r ** 2), X.T @ r / len(y)


def poisoned_batch(rng, step, bad_steps):
    """The batch for a step; during bad_steps the targets are garbage."""
    X, y = batch(rng)
    if step in bad_steps:
        y = 1000.0 * np.ones_like(y)
    return X, y


def run(steps, bad_steps, lr=0.1, every=20, window=10, k=6.0, skip_ahead=10, recover=True, seed=0):
    """SGD on the regression stream; step t's batch comes from np.random.default_rng([seed, t]),
    so any step's data can be regenerated or skipped. Save w every `every` steps. If recover, check
    each step's loss before updating: when it exceeds the mean of the previous `window` kept losses
    by k standard deviations, restore the checkpoint rollback_point gives, skip every step from
    there up to skip_ahead steps past the flagged one (the run never knows which batches were bad),
    and continue. Return (final w, list of flagged steps)."""
    w = np.zeros(3)
    history = []
    ckpts = {0: w.copy()}
    skip = set()
    flagged = []
    step = 0
    while step < steps:
        step += 1
        if step in skip:
            continue
        X, y = poisoned_batch(np.random.default_rng([seed, step]), step, bad_steps)
        loss, g = loss_grad(w, X, y)
        if recover and len(history) >= window:
            prev = np.array([l for _, l in history[-window:]])
            if loss > prev.mean() + k * prev.std():
                back = (step - 2) // every * every
                w = ckpts[back].copy()
                skip |= set(range(back + 1, step + skip_ahead + 1))
                history = [(s, l) for s, l in history if s <= back]
                flagged.append(step)
                step = back
                continue
        history.append((step, loss))
        w = w - lr * g
        if step % every == 0:
            ckpts[step] = w.copy()
    return w, flagged
