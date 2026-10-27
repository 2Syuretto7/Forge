import numpy as np
import sub


def test_folds_partition_the_data():
    folds = sub.kfold_indices(23, 5, seed=1)
    assert len(folds) == 5
    val = np.concatenate([v for _, v in folds])
    assert sorted(val.tolist()) == list(range(23))
    for tr, va in folds:
        assert len(set(tr) & set(va)) == 0 and len(tr) + len(va) == 23


def test_cv_tracks_true_risk():
    rng = np.random.default_rng(5)
    x = rng.uniform(-1, 1, 60)
    y = np.sin(np.pi * x) + 0.3 * rng.normal(size=60)
    s_low = sub.cv_mse(x, y, 1, 5, 0)
    s_good = sub.cv_mse(x, y, 5, 5, 0)
    assert s_good < s_low
    assert 0.05 < s_good < 0.2
