def prob(space, A):
    """P(A)."""
    raise NotImplementedError


def conditional(space, A, B):
    """P(A | B)."""
    raise NotImplementedError


def independent(space, A, B, tol=1e-12):
    """Whether P(A and B) = P(A) P(B)."""
    raise NotImplementedError


def two_dice():
    """Ordered pairs of fair dice."""
    raise NotImplementedError
