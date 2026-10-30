import math

TARGETS = {
    "hill": (lambda x: math.exp(-x * x), -3.0, 3.0, 0.01),
    "sine": (math.sin, 0.0, 2 * math.pi, 0.005),
    "cubic": (lambda x: x ** 3 / 9, -3.0, 3.0, 0.01),
    "kink": (lambda x: abs(x) - 0.5, -2.0, 2.0, 1e-9),
    "root": (math.sqrt, 0.0, 4.0, 0.02),
}


def max_gap(f, a, b, m=60):
    """Largest gap between f and its chord on [a, b], at m points."""
    raise NotImplementedError


def adaptive_knots(f, a, b, tol):
    """Corners from splitting the worst piece at its midpoint until every gap is within tol."""
    raise NotImplementedError


def to_relus(f, knots):
    """(intercept, slope, inner_knots, weights) through (t, f(t)) for the corners."""
    raise NotImplementedError


def evaluate(desc, x):
    """Value of a ReLU description at x."""
    raise NotImplementedError


def build_all(targets):
    """Name -> corners for each target."""
    raise NotImplementedError


# your answer
REPORT = """
"""
