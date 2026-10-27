import numpy as np
import sub

X, Y = sub.make_spiral()


def test_grad_engine_equals_handwritten():
    m = sub.MLP([2, 16, 16, 3], seed=5)
    m.zero_grad()
    sub.cross_entropy_fused(m(sub.Tensor(X)), Y).backward()
    manual = sub.manual_grads(m, X, Y)
    for layer, (dW, db) in zip(m.layers, manual):
        assert np.allclose(layer.W.grad, dW, atol=1e-12)
        assert np.allclose(layer.b.grad, db, atol=1e-12)


def test_losses_recorded():
    _, losses = sub.train([2, 8, 3], X, Y, 0.5, 5)
    assert len(losses) == 5 and all(isinstance(v, float) for v in losses)
    assert abs(losses[0] - np.log(3)) < 0.6


def test_spiral_learned():
    model, losses = sub.train([2, 64, 3], X, Y, 1.0, 300)
    acc = np.mean(model(sub.Tensor(X)).data.argmax(axis=1) == Y)
    assert losses[-1] < 0.5 * losses[0], (losses[0], losses[-1])
    assert acc >= 0.9, acc
