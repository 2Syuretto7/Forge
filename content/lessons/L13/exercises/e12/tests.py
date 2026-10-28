import numpy as np
import sub

rng = np.random.default_rng(12)
X = rng.normal(size=(6, 4))
Wq, Wk, Wv = (rng.normal(size=(4, 4)) for _ in range(3))


def _attn(mask):
    def f(X):
        S = (X @ Wq) @ (X @ Wk).T / 2.0
        S = np.where(mask(X.shape[0]), -np.inf, S)
        return sub.softmax_rows(S) @ (X @ Wv)
    return f


def test_correct_mask_does_not_leak():
    correct = lambda n: np.triu(np.ones((n, n), dtype=bool), k=1)
    assert sub.leaks_future(_attn(correct), X) is False


def test_off_by_one_mask_leaks():
    m = sub.off_by_one_mask(4)
    assert m.tolist() == [[False, False, True, True], [False, False, False, True], [False] * 4, [False] * 4]
    assert sub.leaks_future(_attn(sub.off_by_one_mask), X) is True


def test_no_mask_leaks():
    assert sub.leaks_future(_attn(lambda n: np.zeros((n, n), dtype=bool)), X) is True
