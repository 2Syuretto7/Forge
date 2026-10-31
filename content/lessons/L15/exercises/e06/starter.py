import copy
import numpy as np

TRUE_W = np.array([1.0, -2.0, 0.5])


def batch(rng, n=16):
    """A regression batch drawn from the trainer's generator."""
    X = rng.normal(size=(n, 3))
    return X, X @ TRUE_W + 0.1 * rng.normal(size=n)


def loss_grad(w, X, y):
    """0.5 * mean((X w - y)^2) and its gradient."""
    raise NotImplementedError


def new_state(seed):
    """Everything a run carries: weights, Adam moments and step, and the data generator."""
    raise NotImplementedError


def train_steps(state, n, lr=0.05):
    """Run n Adam steps on fresh batches from state["rng"], updating state in place."""
    raise NotImplementedError


def save(state):
    """A checkpoint that shares nothing with the live state: copies of the arrays, the step and the
    generator's bit_generator.state."""
    raise NotImplementedError


def load(ckpt):
    """A live state from a checkpoint."""
    raise NotImplementedError
