import numpy as np
import sub


def test_update_has_the_requested_spectrum():
    M = sub.target_update(12, 5, seed=1)
    S = np.linalg.svd(M, compute_uv=False)
    assert np.allclose(S[:5], 0.7 ** np.arange(5)) and np.allclose(S[5:], 0)


def test_error_by_rank():
    M = sub.target_update(12, 5, seed=1)
    errs = sub.error_by_rank(M, [0, 1, 2, 5, 8])
    assert errs[0] == 1.0 and errs[3] < 1e-12 and errs[4] < 1e-12
    assert errs[1] > errs[2] > errs[3]
    assert errs[1] > 0.5
