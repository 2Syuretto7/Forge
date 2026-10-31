import numpy as np


def law(N, D, E, A, B, alpha, beta):
    """The parametric loss L(N, D) = E + A N^-alpha + B D^-beta."""
    return E + A * N ** -alpha + B * D ** -beta


def effective_tokens(unique, epochs, r_star=15.4):
    """Unique tokens seen `epochs` times are worth U + U R* (1 - exp(-R / R*)) fresh tokens,
    with R = epochs - 1 repetitions."""
    R = epochs - 1
    return unique + unique * r_star * (1 - np.exp(-R / r_star))


def loss_with_repeats(N, unique, epochs, E, A, B, alpha, beta, r_star=15.4):
    """The parametric loss with D replaced by the effective number of tokens."""
    return law(N, effective_tokens(unique, epochs, r_star), E, A, B, alpha, beta)
