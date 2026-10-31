import numpy as np


def train_bandit(means, steps, lr, use_baseline, rng, noise=1.0):
    """REINFORCE on a Gaussian bandit; returns the final arm probabilities."""
    raise NotImplementedError


def best_arm_prob(probs, means):
    """Probability on the arm with the highest mean."""
    raise NotImplementedError
