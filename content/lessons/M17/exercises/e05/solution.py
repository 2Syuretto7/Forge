import math


def F1(x):
    """Antiderivative of x e^x."""
    return (x - 1) * math.exp(x)


def F2(x):
    """Antiderivative of ln x."""
    return x * math.log(x) - x


def F3(x):
    """Antiderivative of x sin x."""
    return math.sin(x) - x * math.cos(x)


def F4(x):
    """Antiderivative of 2x / (1 + x^2)."""
    return math.log(1 + x * x)


def F5(x):
    """Antiderivative of cos(x) e^(sin x)."""
    return math.exp(math.sin(x))


def definite(F, a, b):
    """F(b) - F(a)."""
    return F(b) - F(a)
