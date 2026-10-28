def candidate_probability(s, bands, rows):
    """Probability that two documents with Jaccard similarity s share at least one band, with the
    signature split into `bands` bands of `rows` rows."""
    raise NotImplementedError


def dprob_ds(s, bands, rows):
    """The derivative of candidate_probability with respect to s."""
    raise NotImplementedError


def threshold(bands, rows):
    """The similarity where the S-curve is steepest, approximately (1 / bands) ** (1 / rows)."""
    raise NotImplementedError


def choose_bands(num_perm, target):
    """Among the (bands, rows) with bands * rows == num_perm, the pair whose threshold is closest
    to target."""
    raise NotImplementedError
