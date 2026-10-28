import numpy as np
import sub

means = [0.0, 0.5, 1.0, 0.2]


def test_collapse_without_kl():
    p0 = sub.train_with_kl(means, 0.0)
    p1 = sub.train_with_kl(means, 0.5)
    assert sub.entropy(p0) < 0.05 and sub.entropy(p1) > 1.0
    opt = 0.25 * np.exp(np.array(means) / 0.5)
    assert np.allclose(p1, opt / opt.sum(), atol=1e-4)
