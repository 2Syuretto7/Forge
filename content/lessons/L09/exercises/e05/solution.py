import numpy as np


def rosenbrock_fg(p, a=1.0, b=100.0):
    """f(x, y) = (a - x)^2 + b (y - x^2)^2 and its gradient."""
    x, y = p
    r = y - x * x
    f = (a - x) ** 2 + b * r * r
    return f, np.array([-2.0 * (a - x) - 4.0 * b * x * r, 2.0 * b * r])


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
