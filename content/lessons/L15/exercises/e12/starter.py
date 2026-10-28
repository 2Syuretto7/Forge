import numpy as np


def sweep_loss(N, lr):
    """A model of a learning-rate sweep: the best loss for size N is 1.7 + 30 N^-0.25, reached at
    lr*(N) = 3e-3 (N / 1e6)^-0.5; away from lr* the loss grows with the squared log ratio."""
    best_lr = 3e-3 * (N / 1e6) ** -0.5
    return 1.7 + 30 * N ** -0.25 + 0.08 * np.log(lr / best_lr) ** 2


LRS = 3e-3 * 2.0 ** np.arange(-6, 3)
SIZES = np.array([1e6, 3e6, 1e7, 3e7, 1e8])


def tuned_losses(sizes, lrs):
    """For each size, the best loss over the learning rates in the sweep, and that rate."""
    raise NotImplementedError


def fixed_lr_losses(sizes, lr):
    """The loss of each size trained at one learning rate."""
    raise NotImplementedError


def fitted_exponent(sizes, losses, E):
    """The exponent a in L - E = k N^-a, by a log-log line."""
    raise NotImplementedError
