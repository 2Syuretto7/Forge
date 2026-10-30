def alternating(n):
    """First n terms of 1 - 1/2 + 1/3 - ..."""
    return sum((-1) ** (k + 1) / k for k in range(1, n + 1))


def one_up_two_down(blocks):
    """Sum of blocks of 1/(2j-1) - 1/(4j-2) - 1/(4j)."""
    s = 0.0
    for j in range(1, blocks + 1):
        s += 1 / (2 * j - 1) - 1 / (4 * j - 2) - 1 / (4 * j)
    return s


def steer(target, n_terms):
    """Riemann's rearrangement toward target, after n_terms terms."""
    s, odd, even = 0.0, 1, 2
    for _ in range(n_terms):
        if s <= target:
            s += 1 / odd
            odd += 2
        else:
            s -= 1 / even
            even += 2
    return s
