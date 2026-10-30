import numpy as np


def _softmax(z):
    raise NotImplementedError


def cross_entropy(z, c):
    """-log softmax(z)[c], computed stably."""
    raise NotImplementedError


def cross_entropy_grad(z, c):
    """p - y."""
    raise NotImplementedError


def chain_check(z, c):
    """Log VJP followed by softmax VJP."""
    raise NotImplementedError
