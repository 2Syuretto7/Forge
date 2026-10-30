import numpy as np
import sub

X = np.array([4.0, 1.0, 0.0, 2.0, -1.0, 9.0])


def test_silent_failures():
    assert list(sub.silent_failures(X)) == [2, 4]


def test_one_bad_value_poisons_the_mean():
    m = sub.poisoned_mean(X)
    assert not np.isfinite(m)
    assert np.isfinite(sub.poisoned_mean(np.array([1.0, 2.0])))


def test_strict_log():
    assert np.allclose(sub.strict_log(np.array([1.0, np.e])), [0, 1])
    try:
        sub.strict_log(X)
    except ValueError as e:
        assert "2 entries" in str(e) and "index 2" in str(e)
        return
    raise AssertionError("strict_log should refuse non-positive entries")
