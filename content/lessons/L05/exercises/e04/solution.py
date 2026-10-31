import numpy as np


def ema(xs, beta, debias=False):
    """m_t = beta m_{t-1} + (1 - beta) x_t from m_0 = 0, for t = 1..len(xs).
    With debias=True, divide m_t by 1 - beta**t."""
    out = np.zeros(len(xs))
    m = 0.0
    for t, x in enumerate(xs, start=1):
        m = beta * m + (1.0 - beta) * x
        out[t - 1] = m / (1.0 - beta ** t) if debias else m
    return out


def momentum_gain(beta, omega):
    """Steady-state amplitude of v_t = beta v_{t-1} + g_t for the input g_t = cos(omega t)."""
    return 1.0 / abs(1.0 - beta * np.exp(-1j * omega))


def ema_gain(beta, omega):
    """The same for the EMA, which is the momentum sum scaled by 1 - beta."""
    return (1.0 - beta) * momentum_gain(beta, omega)
