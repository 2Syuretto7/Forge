import numpy as np
import sub

rng = np.random.default_rng(4)
X = rng.normal(size=(10, 3))
y = rng.normal(size=10)


def test_grad_loss():
    w = rng.normal(size=3)
    _, g = sub.loss_grad(w, X, y)
    num = [(sub.loss_grad(w + e, X, y)[0] - sub.loss_grad(w - e, X, y)[0]) / 2e-6 for e in np.eye(3) * 1e-6]
    assert np.allclose(g, num, atol=1e-8)


def test_exact_resume():
    straight = sub.train_steps(sub.new_state(0), 100)["w"]
    state = sub.train_steps(sub.new_state(0), 40)
    ckpt = sub.save(state)
    sub.train_steps(state, 5)
    resumed = sub.train_steps(sub.load(ckpt), 60)
    assert np.array_equal(resumed["w"], straight) and resumed["step"] == 100
    assert np.abs(straight - sub.TRUE_W).max() < 0.1
