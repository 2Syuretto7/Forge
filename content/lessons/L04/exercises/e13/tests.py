import numpy as np
import sub


def _mlp_forward(x):
    W = sub.Tensor(np.ones((3, 4)))
    return (x @ W).relu().sum()


def test_default_on():
    assert sub.is_grad_enabled() is True


def test_no_graph_inside():
    x = sub.Tensor(np.ones((2, 3)))
    with sub.no_grad():
        assert sub.is_grad_enabled() is False
        y = _mlp_forward(x)
    assert y._parents == () and y._backward is None
    assert sub.is_grad_enabled() is True


def test_grad_resumes_after_block():
    x = sub.Tensor(np.ones((2, 3)))
    with sub.no_grad():
        _mlp_forward(x)
    _mlp_forward(x).backward()
    assert np.allclose(x.grad, 4.0)


def test_nested_and_exceptions():
    with sub.no_grad():
        with sub.no_grad():
            pass
        assert sub.is_grad_enabled() is False
    assert sub.is_grad_enabled() is True
    try:
        with sub.no_grad():
            raise KeyError("boom")
    except KeyError:
        pass
    assert sub.is_grad_enabled() is True
