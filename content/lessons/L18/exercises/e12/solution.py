import numpy as np


def correct_average(grad_sums, counts):
    """Each rank holds the SUM of its examples' gradients and its example count. The full-batch
    mean gradient is the sum over ranks divided by the total count."""
    return sum(grad_sums) / sum(counts)


def mean_of_means(grad_sums, counts):
    """A common bug: average the ranks' mean gradients, which weights a rank with few examples as
    much as one with many."""
    return sum(g / c for g, c in zip(grad_sums, counts)) / len(counts)


def sum_of_means(grad_sums, counts):
    """Another bug: all-reduce with a sum and forget to divide by the number of ranks."""
    return sum(g / c for g, c in zip(grad_sums, counts))
