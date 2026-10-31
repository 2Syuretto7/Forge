import math
import numpy as np


def select_and_report(k, n, rng, delta=0.05):
    """Best test accuracy of k random models, with a single-model Hoeffding interval."""
    raise NotImplementedError


def fresh_accuracy(n, rng):
    """Accuracy of a random-guessing model on a fresh test set."""
    raise NotImplementedError


def honest_interval(reported, n, k, delta=0.05):
    """Interval with the union-bound half-width for k models."""
    raise NotImplementedError
