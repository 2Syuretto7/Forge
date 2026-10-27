import numpy as np


def init_mlp(sizes, seed=0):
    rng = np.random.default_rng(seed)
    p = {}
    for i, (a, b) in enumerate(zip(sizes, sizes[1:]), start=1):
        p[f"W{i}"] = rng.normal(size=(a, b)) * np.sqrt(2.0 / a)
        p[f"b{i}"] = np.zeros(b)
    return p


def loss_and_grads(params, X, y, act="relu"):
    raise NotImplementedError


def predict(params, X, act="relu"):
    raise NotImplementedError


def sgd_step(params, grads, lr):
    raise NotImplementedError


def train(params, X, y, lr=1.0, epochs=200, batch=32, seed=0, act="relu"):
    raise NotImplementedError
