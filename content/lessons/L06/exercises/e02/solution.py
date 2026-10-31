import numpy as np


class BatchNorm:
    """Batch norm with running statistics for evaluation, as in PyTorch's BatchNorm1d."""

    def __init__(self, n, momentum=0.1, eps=1e-5):
        self.gamma, self.beta = np.ones(n), np.zeros(n)
        self.running_mean, self.running_var = np.zeros(n), np.ones(n)
        self.momentum, self.eps = momentum, eps
        self.training = True

    def forward(self, x):
        if self.training:
            mu, var = x.mean(axis=0), x.var(axis=0)
            n = x.shape[0]
            m = self.momentum
            self.running_mean = (1 - m) * self.running_mean + m * mu
            self.running_var = (1 - m) * self.running_var + m * var * n / (n - 1)
        else:
            mu, var = self.running_mean, self.running_var
        return self.gamma * (x - mu) / np.sqrt(var + self.eps) + self.beta
