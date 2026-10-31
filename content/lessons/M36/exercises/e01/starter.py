import math
import numpy as np


def sigmoid(t):
    """Logistic function."""
    raise NotImplementedError


def log_prob(x, theta):
    """log p_theta(x) for x in {0, 1}."""
    raise NotImplementedError


def score(x, theta):
    """Derivative of log p_theta(x) in theta."""
    raise NotImplementedError


def exact_grad(theta, r1, r0):
    """Gradient of the expected reward."""
    raise NotImplementedError


def estimate_grad(theta, r1, r0, n, rng):
    """Score-function estimate of the gradient."""
    raise NotImplementedError
