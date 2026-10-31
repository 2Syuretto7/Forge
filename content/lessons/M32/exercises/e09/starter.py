import math
import numpy as np


def scaled_walk(n, T, paths, rng):
    """Random walks with n steps per unit time, scaled by 1/sqrt(n)."""
    raise NotImplementedError


def heat_kernel(x, t):
    """The N(0, t) density."""
    raise NotImplementedError


def d_heat_dx(x, t):
    """d/dx of the heat kernel."""
    raise NotImplementedError


def d2_heat_dx2(x, t):
    """d^2/dx^2 of the heat kernel."""
    raise NotImplementedError


def d_heat_dt(x, t):
    """d/dt of the heat kernel."""
    raise NotImplementedError
