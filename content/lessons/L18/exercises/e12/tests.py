import numpy as np
import sub

rng = np.random.default_rng(6)
grads = rng.normal(size=(10, 3))
counts = [4, 4, 2]
sums = [grads[:4].sum(0), grads[4:8].sum(0), grads[8:].sum(0)]


def test_correct():
    assert np.allclose(sub.correct_average(sums, counts), grads.mean(0))


def test_bugs():
    assert not np.allclose(sub.mean_of_means(sums, counts), grads.mean(0))
    equal = [grads[:5].sum(0), grads[5:].sum(0)]
    assert np.allclose(sub.mean_of_means(equal, [5, 5]), grads.mean(0))
    assert np.allclose(sub.sum_of_means(equal, [5, 5]), 2 * grads.mean(0))
