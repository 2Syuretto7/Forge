import math


def transformed_density(p_x, g_inv, g_inv_prime):
    """y -> p_X(g^-1(y)) |g^-1'(y)|."""
    raise NotImplementedError


def density_of_square(y):
    """Density of X^2 for uniform X."""
    raise NotImplementedError


def density_of_neglog(y):
    """Density of -ln X for uniform X."""
    raise NotImplementedError


def lognormal_density(y):
    """Density of e^Z for standard normal Z."""
    raise NotImplementedError
