import numpy as np
import sub

rng = np.random.default_rng(5)
Ws = [rng.normal(size=(4, 4)) * 0.6 for _ in range(16)]
x = rng.normal(size=(3, 4))
dout = rng.normal(size=(3, 4))


def test_grad_checkpointed():
    grads, _ = sub.checkpointed_grads(x, Ws, dout, 4)
    for layer, (i, j) in [(0, (1, 2)), (7, (0, 0)), (15, (3, 1))]:
        P = [w.copy() for w in Ws]
        P[layer][i, j] += 1e-6
        up = np.sum(sub.forward(x, P)[-1] * dout)
        P[layer][i, j] -= 2e-6
        down = np.sum(sub.forward(x, P)[-1] * dout)
        assert abs((up - down) / 2e-6 - grads[layer][i, j]) < 1e-6


def test_same_as_plain_backward():
    plain = sub.backward(sub.forward(x, Ws), Ws, dout)
    for k in [1, 2, 4, 8, 16]:
        grads, _ = sub.checkpointed_grads(x, Ws, dout, k)
        assert all(np.allclose(a, b) for a, b in zip(plain, grads))


def test_square_root_rule():
    peaks = {k: sub.checkpointed_grads(x, Ws, dout, k)[1] for k in [1, 2, 4, 8, 16]}
    assert peaks[1] == 17 and peaks[4] == min(peaks.values()) and peaks[4] < peaks[16]
