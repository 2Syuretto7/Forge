import numpy as np


class SGD:
    """SGD with optional heavy-ball momentum and L2 weight decay on the weights (keys starting with "W")."""

    def __init__(self, lr, momentum=0.0, weight_decay=0.0):
        self.lr, self.momentum, self.weight_decay = lr, momentum, weight_decay
        self.v = {}

    def step(self, params, grads, lr=None):
        lr = self.lr if lr is None else lr
        for k in params:
            g = grads[k]
            if self.weight_decay and k.startswith("W"):
                g = g + self.weight_decay * params[k]
            if self.momentum:
                self.v[k] = self.momentum * self.v.get(k, 0.0) + g
                g = self.v[k]
            params[k] -= lr * g


class Adam:
    """Adam on a dict of arrays. weight_decay applies to the weights only, either decoupled
    (AdamW) or as an L2 term added to the gradient."""

    def __init__(self, lr, b1=0.9, b2=0.999, eps=1e-8, weight_decay=0.0, decoupled=True, bias_correction=True):
        self.lr, self.b1, self.b2, self.eps = lr, b1, b2, eps
        self.weight_decay, self.decoupled, self.bias_correction = weight_decay, decoupled, bias_correction
        self.m, self.v, self.t = {}, {}, 0

    def step(self, params, grads, lr=None):
        lr = self.lr if lr is None else lr
        self.t += 1
        c1 = 1.0 - self.b1 ** self.t if self.bias_correction else 1.0
        c2 = 1.0 - self.b2 ** self.t if self.bias_correction else 1.0
        for k in params:
            g = grads[k]
            wd = self.weight_decay if k.startswith("W") else 0.0
            if wd and not self.decoupled:
                g = g + wd * params[k]
            self.m[k] = self.b1 * self.m.get(k, 0.0) + (1.0 - self.b1) * g
            self.v[k] = self.b2 * self.v.get(k, 0.0) + (1.0 - self.b2) * g * g
            if wd and self.decoupled:
                params[k] -= lr * wd * params[k]
            params[k] -= lr * (self.m[k] / c1) / (np.sqrt(self.v[k] / c2) + self.eps)
