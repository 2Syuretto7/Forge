def candidate_probability(s, bands, rows):
    """Probability that two documents with Jaccard similarity s share at least one band, with the
    signature split into `bands` bands of `rows` rows."""
    return 1 - (1 - s ** rows) ** bands


def dprob_ds(s, bands, rows):
    """The derivative of candidate_probability with respect to s."""
    return bands * rows * s ** (rows - 1) * (1 - s ** rows) ** (bands - 1)


def threshold(bands, rows):
    """The similarity where the S-curve is steepest, approximately (1 / bands) ** (1 / rows)."""
    return (1 / bands) ** (1 / rows)


def choose_bands(num_perm, target):
    """Among the (bands, rows) with bands * rows == num_perm, the pair whose threshold is closest
    to target."""
    pairs = [(num_perm // r, r) for r in range(1, num_perm + 1) if num_perm % r == 0]
    return min(pairs, key=lambda p: abs(threshold(*p) - target))
