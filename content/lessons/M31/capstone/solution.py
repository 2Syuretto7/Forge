import math
import numpy as np


# provided
def make_eval(seed=0):
    return (np.random.default_rng(seed).random(2000) < 0.87).astype(float)


def hoeffding_interval(correct, delta=0.05):
    """(accuracy, low, high) from Hoeffding's inequality."""
    c = np.asarray(correct, dtype=float)
    acc = float(c.mean())
    h = math.sqrt(math.log(2 / delta) / (2 * len(c)))
    return acc, acc - h, acc + h


def bootstrap_interval(correct, B=4000, seed=0, level=0.95):
    """(accuracy, low, high) from the percentile bootstrap."""
    c = np.asarray(correct, dtype=float)
    acc = float(c.mean())
    boot = np.random.default_rng(seed).binomial(len(c), acc, size=B) / len(c)
    lo, hi = np.quantile(boot, [(1 - level) / 2, (1 + level) / 2])
    return acc, float(lo), float(hi)


def union_epsilon(n, k, delta=0.05):
    """Half-width that holds for k models at once."""
    return math.sqrt(math.log(2 * k / delta) / (2 * n))


def reuse_experiment(k=1000, n=1000, seed=0):
    """Selecting the best of k random models on one test set, then checking it on another."""
    rng = np.random.default_rng(seed)
    best = float((rng.random((k, n)) < 0.5).mean(axis=1).max())
    fresh = float((rng.random(n) < 0.5).mean())
    return {"best_test": best, "fresh": fresh, "inflation": best - fresh}


# your answer
REPORT = """
The classifier is correct on 87.2 percent of the 2,000 test examples. Hoeffding's inequality
gives a 95 percent interval of plus or minus 3.0 points that holds for any distribution of the
errors, provided the examples are independent; the percentile bootstrap gives a narrower interval
of about plus or minus 1.5 points, which is approximate and relies on the sample representing the
population. Selecting the best of 1,000 models that only guess, using one test set of 1,000
examples, produced a best test accuracy about 5 points above chance, while the same model scored
near 50 percent on a fresh test set: the inflation is pure selection. The union bound says a
half-width of about 7.3 points is needed to cover 1,000 models at once, so the inflation stayed
inside it, as the theory promises. An evaluator should fix the models before touching the test
set, count every model compared, widen the interval by the union bound or hold out a fresh test
set for the final number, and never tune on the data used to report.
"""
