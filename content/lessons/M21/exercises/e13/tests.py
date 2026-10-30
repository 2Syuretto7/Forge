import numpy as np
import sub

M = {"log_prior": np.log([0.6, 0.4]), "log_word": np.log(np.array([[0.5, 0.3, 0.2], [0.2, 0.3, 0.5]]))}


def test_doubling():
    x = np.array([0, 1, 2])
    assert np.isclose(sub.prior_free_part(M, 2 * x), 2 * sub.prior_free_part(M, x))
    before, after = sub.confidence_after_duplication(M, x)
    assert after > before > 0.5
