import numpy as np


def emitted_distribution(p, q):
    """Speculative decoding's rule for one token: draw x from the draft q, accept it with
    probability min(1, p(x)/q(x)), otherwise draw from max(0, p - q) renormalized. Return the
    exact distribution of the emitted token."""
    raise NotImplementedError


def acceptance_rate(p, q):
    """The probability the draft's token is accepted: sum min(p, q) = 1 - total variation."""
    raise NotImplementedError


def acceptance_grad(p, z):
    """The gradient of acceptance_rate(p, softmax(z)) with respect to the draft's logits z."""
    raise NotImplementedError


def expected_tokens(alpha, gamma):
    """Tokens produced per target-model call when gamma draft tokens are each accepted with
    probability alpha: (1 - alpha^(gamma + 1)) / (1 - alpha)."""
    raise NotImplementedError
