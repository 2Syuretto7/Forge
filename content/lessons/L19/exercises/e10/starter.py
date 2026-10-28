import numpy as np


def update_ratios(params, updates):
    """For each named parameter, |update| / |parameter| (Frobenius norms): how far one step moves it."""
    raise NotImplementedError


def flag_layers(ratios, low=1e-5, high=1e-2):
    """Names whose ratio is outside [low, high]: barely training, or moving too fast to be stable."""
    raise NotImplementedError
