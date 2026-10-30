def prob(space, A):
    """P(A)."""
    return sum(space[w] for w in A)


def conditional(space, A, B):
    """P(A | B)."""
    pb = prob(space, B)
    if pb == 0:
        raise ValueError("conditioning on an event of probability 0")
    return prob(space, A & B) / pb


def independent(space, A, B, tol=1e-12):
    """Whether P(A and B) = P(A) P(B)."""
    return abs(prob(space, A & B) - prob(space, A) * prob(space, B)) <= tol


def two_dice():
    """Ordered pairs of fair dice."""
    return {(i, j): 1 / 36 for i in range(1, 7) for j in range(1, 7)}
