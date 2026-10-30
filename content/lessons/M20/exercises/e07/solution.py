import numpy as np


def histogram_density(samples, bins, lo, hi):
    """(bin centers, estimated density)."""
    counts, edges = np.histogram(samples, bins=bins, range=(lo, hi))
    w = edges[1] - edges[0]
    return (edges[:-1] + edges[1:]) / 2, counts / (len(samples) * w)


def max_relative_deviation(samples, pdf, bins, lo, hi, min_expected=1000):
    """Worst relative deviation over well-filled bins."""
    counts, edges = np.histogram(samples, bins=bins, range=(lo, hi))
    centers = (edges[:-1] + edges[1:]) / 2
    expected = len(samples) * pdf(centers) * (edges[1] - edges[0])
    ok = expected >= min_expected
    return float(np.max(np.abs(counts[ok] - expected[ok]) / expected[ok]))
