import numpy as np


class Adam:
    """Adam for a single array. step(x, g) returns the updated array."""

    def __init__(self, lr, b1=0.9, b2=0.999, eps=1e-8, bias_correction=True):
        self.lr, self.b1, self.b2, self.eps = lr, b1, b2, eps
        self.bias_correction = bias_correction
        self.m = self.v = None
        self.t = 0

    def step(self, x, g):
        if self.m is None:
            self.m, self.v = np.zeros_like(g), np.zeros_like(g)
        self.t += 1
        self.m = self.b1 * self.m + (1.0 - self.b1) * g
        self.v = self.b2 * self.v + (1.0 - self.b2) * g * g
        m, v = self.m, self.v
        if self.bias_correction:
            m = m / (1.0 - self.b1 ** self.t)
            v = v / (1.0 - self.b2 ** self.t)
        return x - self.lr * m / (np.sqrt(v) + self.eps)


def uncorrected_factor(t, b1=0.9, b2=0.999):
    """How many times larger step t is without bias correction: (1 - b1^t) / sqrt(1 - b2^t)."""
    return (1.0 - b1 ** t) / np.sqrt(1.0 - b2 ** t)


def peak(b1=0.9, b2=0.999, tmax=10000):
    """The step t in 1..tmax where the factor is largest, and its value."""
    t = np.arange(1, tmax + 1)
    f = uncorrected_factor(t, b1, b2)
    i = int(np.argmax(f))
    return int(t[i]), float(f[i])


def measured_factor(t, b1=0.9, b2=0.999, g=1.0):
    """Run Adam with and without correction on a constant gradient g for t steps and return the
    ratio of the sizes of their t-th steps."""
    sizes = []
    for corr in (False, True):
        opt = Adam(1e-3, b1, b2, eps=0.0, bias_correction=corr)
        x = np.zeros(1)
        for _ in range(t):
            new = opt.step(x, np.array([g]))
            last = abs(new[0] - x[0])
            x = new
        sizes.append(last)
    return sizes[0] / sizes[1]
