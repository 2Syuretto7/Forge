import numpy as np


def terms(n):
    """float32 array of 1/k^2 for k = 1..n."""
    raise NotImplementedError


def forward(t):
    """Sum in order, first term first, in float32."""
    raise NotImplementedError


def backward(t):
    """Sum from the last term to the first, in float32."""
    raise NotImplementedError


def errors(n):
    """(forward error, backward error) against the float64 sum of the same terms."""
    raise NotImplementedError
