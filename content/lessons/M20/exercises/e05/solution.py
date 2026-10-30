import math


def transformed_density(p_x, g_inv, g_inv_prime):
    """y -> p_X(g^-1(y)) |g^-1'(y)|."""
    return lambda y: p_x(g_inv(y)) * abs(g_inv_prime(y))


def density_of_square(y):
    """Density of X^2 for uniform X."""
    return 0.5 / math.sqrt(y)


def density_of_neglog(y):
    """Density of -ln X for uniform X."""
    return math.exp(-y)


def lognormal_density(y):
    """Density of e^Z for standard normal Z."""
    return math.exp(-math.log(y) ** 2 / 2) / (y * math.sqrt(2 * math.pi))
