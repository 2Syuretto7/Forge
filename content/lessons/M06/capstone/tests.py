import numpy as np
import sub

DATA = sub.make_datasets(0)
FOUND = sub.detect(DATA)


def test_fit_line():
    s, c, r2 = sub.fit_line(np.array([0.0, 1, 2]), np.array([1.0, 3, 5]))
    assert abs(s - 2) < 1e-12 and abs(c - 1) < 1e-12 and abs(r2 - 1) < 1e-12


def test_every_law_is_classified():
    assert [law for law, _ in FOUND] == [law for law, _ in sub.LAWS]


def test_every_parameter_within_five_percent():
    for (law, got), (_, true) in zip(FOUND, sub.LAWS):
        assert set(got) == set(true), law
        for k, v in true.items():
            assert abs(got[k] / v - 1) < 0.05, f"{law} {k}: {got[k]:.4g} vs {v}"


def test_a_different_seed():
    for (law, _), (true_law, _) in zip(sub.detect(sub.make_datasets(7)), sub.LAWS):
        assert law == true_law
