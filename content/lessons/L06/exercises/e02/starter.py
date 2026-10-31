import numpy as np


class BatchNorm:
    """Batch norm with running statistics for evaluation, as in PyTorch's BatchNorm1d."""

    def __init__(self, n, momentum=0.1, eps=1e-5):
        self.gamma, self.beta = np.ones(n), np.zeros(n)
        self.running_mean, self.running_var = np.zeros(n), np.ones(n)
        self.momentum, self.eps = momentum, eps
        self.training = True

    def forward(self, x):
        raise NotImplementedError
