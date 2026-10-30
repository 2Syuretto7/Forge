import math


def log10_comb(n, k):
    """log10 of n choose k via log-gamma."""
    return (math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)) / math.log(10)


def digits_of_comb(n, k):
    """Decimal digits of n choose k."""
    return math.floor(log10_comb(n, k)) + 1


def steps_per_epoch(n, batch):
    """Mini-batches to see n examples once."""
    return math.ceil(n / batch)


def epochs_before_repeat_is_likely(n, batch):
    """log10 of the number of random batches before a repeat is likely."""
    return 0.5 * math.log10(2 * math.log(2)) + 0.5 * log10_comb(n, batch)
