import numpy as np


def update_ratios(params, updates):
    """For each named parameter, |update| / |parameter| (Frobenius norms): how far one step moves it."""
    return {name: float(np.linalg.norm(updates[name]) / np.linalg.norm(params[name])) for name in params}


def flag_layers(ratios, low=1e-5, high=1e-2):
    """Names whose ratio is outside [low, high]: barely training, or moving too fast to be stable."""
    return sorted(n for n, r in ratios.items() if not low <= r <= high)
