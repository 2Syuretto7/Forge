import numpy as np
import sub

W = np.array([0.3, 0.3, 0.4])
M = np.array([[-2.0, 0.0], [2.0, 1.0], [0.0, -2.0]])


def sample(n, rng):
    k = rng.choice(3, size=n, p=W)
    return M[k] + 0.35 * rng.standard_normal((n, 2))


def test_memorization():
    rng = np.random.default_rng(0)
    train = sample(30, rng)
    copies = sub.nn_distance(sub.generate(train, 0.0, 400, rng), train)
    smooth = sub.nn_distance(sub.generate(train, 0.2, 400, rng), train)
    fresh = sub.nn_distance(sample(400, rng), train)
    assert copies < 0.03 and smooth > 3 * copies and smooth > 0.5 * fresh, (copies, smooth, fresh)
