import math

import numpy as np


def expected_colliding_pairs(n, bits):
    """C(n, 2) / 2**bits."""
    raise NotImplementedError


def p_any_collision(n, bits):
    """1 - exp(-C(n, 2) / 2**bits)."""
    raise NotImplementedError


def simulated_colliding_pairs(n, bits, seed=0):
    """Colliding pairs among n uniform random hash values of the given width."""
    raise NotImplementedError
