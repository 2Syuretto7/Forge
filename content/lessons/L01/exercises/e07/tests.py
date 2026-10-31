import numpy as np
import sub

rng = np.random.default_rng(7)
Xtr = rng.normal(size=(100, 3)) * np.array([1.0, 1000.0, 0.01]) + np.array([5.0, -300.0, 2.0])
Xte = rng.normal(size=(40, 3)) * np.array([1.0, 1000.0, 0.01]) + np.array([5.0, -300.0, 2.0])


def test_training_columns_are_standardized():
    A, _ = sub.fit_transform_both(Xtr, Xte)
    assert np.allclose(A.mean(axis=0), 0, atol=1e-12)
    assert np.allclose(A.std(axis=0), 1, atol=1e-12)


def test_test_split_uses_training_statistics():
    _, B = sub.fit_transform_both(Xtr, Xte)
    mean, std = Xtr.mean(axis=0), Xtr.std(axis=0)
    assert np.allclose(B, (Xte - mean) / std)
    assert not np.allclose(B.mean(axis=0), 0, atol=1e-6), "test statistics must not be used"


def test_constant_feature():
    C = np.column_stack([Xtr[:, 0], np.full(100, 7.0)])
    m, s = sub.fit_standardizer(C)
    assert s[1] == 1.0
    assert np.all(np.isfinite(sub.transform(C, m, s)))
