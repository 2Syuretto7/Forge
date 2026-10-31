import numpy as np


def xavier(n_in, n_out, rng):
    """Normal weights with variance 2 / (n_in + n_out)."""
    return rng.normal(size=(n_in, n_out)) * np.sqrt(2.0 / (n_in + n_out))


def he(n_in, n_out, rng):
    """Normal weights with variance 2 / n_in."""
    return rng.normal(size=(n_in, n_out)) * np.sqrt(2.0 / n_in)


def depth_rms(init, act, depth=30, width=256, batch=128, seed=0):
    """Push unit-normal inputs through `depth` layers h <- act(h W) with W from `init`
    ("xavier", "he" or "unit" for standard normal). Return the RMS of h after each layer."""
    rng = np.random.default_rng(seed)
    h = rng.normal(size=(batch, width))
    phi = np.tanh if act == "tanh" else (lambda z: np.maximum(z, 0.0))
    out = []
    for _ in range(depth):
        if init == "xavier":
            W = xavier(width, width, rng)
        elif init == "he":
            W = he(width, width, rng)
        else:
            W = rng.normal(size=(width, width))
        h = phi(h @ W)
        out.append(float(np.sqrt(np.mean(h * h))))
    return out
