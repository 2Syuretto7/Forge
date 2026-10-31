import numpy as np
import sub


def test_split():
    tr, va = sub.train_val_split(list(range(100)))
    assert list(tr) == list(range(90)) and list(va) == list(range(90, 100))


def test_batches():
    ids = np.arange(1000) * 3
    x, y = sub.get_batch(ids, 16, 8, np.random.default_rng(0))
    assert x.shape == (8, 16) and y.shape == (8, 16)
    assert np.all(y[:, :-1] == x[:, 1:]) and np.all(y - x == 3)
    starts = np.random.default_rng(0).integers(0, 1000 - 16, size=8)
    assert np.all(x[:, 0] == ids[starts])


def test_epoch():
    assert sub.tokens_per_epoch(1_000_000, 128, 32) == 1_000_000 / 4096
