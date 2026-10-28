import numpy as np


def outlier_examples(per_example_loss, k=10.0):
    """Indices of examples whose loss exceeds the median by more than k median absolute
    deviations: robust to the outliers themselves, unlike a mean and standard deviation."""
    raise NotImplementedError
