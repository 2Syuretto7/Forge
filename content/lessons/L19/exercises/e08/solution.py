import numpy as np


def outlier_examples(per_example_loss, k=10.0):
    """Indices of examples whose loss exceeds the median by more than k median absolute
    deviations: robust to the outliers themselves, unlike a mean and standard deviation."""
    x = np.asarray(per_example_loss, dtype=float)
    med = np.median(x)
    mad = np.median(np.abs(x - med))
    return [int(i) for i in np.flatnonzero(x > med + k * max(mad, 1e-12))]
