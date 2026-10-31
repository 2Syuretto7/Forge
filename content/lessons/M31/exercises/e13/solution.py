import math
import numpy as np


def select_and_report(k, n, rng, delta=0.05):
    """Best test accuracy of k random models, with a single-model Hoeffding interval."""
    best = float((rng.random((k, n)) < 0.5).mean(axis=1).max())
    h = math.sqrt(math.log(2 / delta) / (2 * n))
    return best, best - h, best + h


def fresh_accuracy(n, rng):
    """Accuracy of a random-guessing model on a fresh test set."""
    return float((rng.random(n) < 0.5).mean())


def honest_interval(reported, n, k, delta=0.05):
    """Interval with the union-bound half-width for k models."""
    h = math.sqrt(math.log(2 * k / delta) / (2 * n))
    return reported - h, reported + h
