import math

import numpy as np


def ball_volume(n):
    """Volume of the unit ball in n dimensions."""
    raise NotImplementedError


def cube_fraction(n):
    """V_n / 2^n."""
    raise NotImplementedError


def mc_fraction(n, samples, seed=0):
    """(fraction inside, standard error) by sampling the cube."""
    raise NotImplementedError


def peak_dimension(max_n=50):
    """Dimension of largest volume."""
    raise NotImplementedError
