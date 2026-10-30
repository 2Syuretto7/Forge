import math
import sys

EPS = sys.float_info.epsilon

# provided
X = ("x",)


# provided
def c(v):
    return ("c", float(v))


# provided
FUNCTIONS = [
    (("^", X, 2), 1.5),
    (("^", X, 5), -0.7),
    (("sin", X), 0.4),
    (("cos", ("*", c(3), X)), 1.1),
    (("exp", ("*", c(-2), X)), 0.3),
    (("log", X), 2.5),
    (("log", ("+", X, c(1))), 0.01),
    (("tanh", X), 0.8),
    (("/", c(1), X), 0.6),
    (("/", ("sin", X), X), 1.3),
    (("*", X, ("exp", X)), -1.2),
    (("*", ("^", X, 3), ("sin", X)), 2.0),
    (("exp", ("sin", X)), 0.9),
    (("sin", ("exp", X)), 0.5),
    (("log", ("^", X, 2)), 3.0),
    (("tanh", ("*", c(5), X)), 0.1),
    (("/", ("exp", X), ("+", c(1), ("exp", X))), -0.4),
    (("^", ("+", c(1), ("^", X, 2)), -0.5), 0.7),
    (("-", ("*", c(2), X), ("log", X)), 4.0),
    (("*", ("cos", X), ("cos", X)), 0.25),
    (("exp", ("^", X, 2)), 1.4),
    (("log", ("+", c(1), ("exp", X))), -2.0),
    (("/", X, ("+", c(1), ("^", X, 2))), 1.7),
    (("sin", ("sin", ("sin", X))), 1.0),
    (("^", ("sin", X), 3), 0.6),
    (("*", ("exp", ("*", c(-1), X)), ("sin", ("*", c(10), X))), 0.2),
    (("log", ("cos", X)), 0.3),
    (("tanh", ("tanh", X)), -0.6),
    (("/", c(1), ("+", c(1), ("exp", ("*", c(-1), X)))), 0.0),
    (("^", X, 0.5), 9.0),
]


def evaluate(e, x):
    """Value of the tree at x."""
    raise NotImplementedError


def derivative(e):
    """Tree of the derivative."""
    raise NotImplementedError


def budget(e, x, h):
    """Expected error of the central difference at step h."""
    raise NotImplementedError


def best_h(e, x):
    """Step minimizing truncation plus rounding."""
    raise NotImplementedError


def verify(e, x, d=None):
    """(ok, error, allowed) comparing a derivative tree with a central difference."""
    raise NotImplementedError
