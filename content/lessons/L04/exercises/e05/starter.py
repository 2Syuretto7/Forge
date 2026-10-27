import numpy as np


def empirical(data, K):
    raise NotImplementedError


def avg_nll(z, data):
    raise NotImplementedError


def grad_avg_nll(z, data, K):
    raise NotImplementedError


def fit(data, K, steps=2000, lr=1.0):
    raise NotImplementedError
