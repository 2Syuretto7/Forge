import numpy as np
import sub


def test_first_step_and_unbiased():
    g = np.array([1e-6, -3.0, 250.0])
    assert np.allclose(sub.first_step_size(g, 0.01), [0.01 * 1e-6 / (1e-6 + 1e-8), 0.01, 0.01])
    state = {"m": np.zeros(2), "v": np.zeros(2), "t": 0}
    x = np.zeros(2)
    c = np.array([2.0, -0.5])
    for t in range(1, 50):
        x = sub.adam_step(x, c, state, lr=0.1)
        assert np.allclose(state["m"] / (1 - 0.9**t), c) and np.allclose(state["v"] / (1 - 0.999**t), c * c)
    assert np.allclose(x, -0.1 * 49 * np.sign(c), rtol=1e-6)
