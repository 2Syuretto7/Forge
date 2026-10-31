import numpy as np


def ema(xs, beta, debias=False):
    """m_t = beta m_{t-1} + (1 - beta) x_t from m_0 = 0, for t = 1..len(xs).
    With debias=True, divide m_t by 1 - beta**t."""
    raise NotImplementedError


def momentum_gain(beta, omega):
    """Steady-state amplitude of v_t = beta v_{t-1} + g_t for the input g_t = cos(omega t)."""
    raise NotImplementedError


def ema_gain(beta, omega):
    """The same for the EMA, which is the momentum sum scaled by 1 - beta."""
    raise NotImplementedError
