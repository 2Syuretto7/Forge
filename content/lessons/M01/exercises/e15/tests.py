import math
import sub


def test_correct_hours():
    assert math.isclose(sub.gpu_hours(1e8, 2e9, 1e14), 1.2e18 / 1e14 / 3600, rel_tol=1e-12)


def test_the_colleagues_slip():
    assert math.isclose(sub.colleague_gpu_hours(1e8, 2e9, 1e14), 12000, rel_tol=1e-12)
    assert math.isclose(sub.error_factor(1e8, 2e9, 1e14), 3600, rel_tol=1e-9)
    assert sub.diagnose(sub.error_factor(1e8, 2e9, 1e14)) == "seconds vs hours"


def test_diagnose():
    assert sub.diagnose(1 / 8) == "bits vs bytes"
    assert sub.diagnose(1.0737) == "GB vs GiB"
    assert sub.diagnose(1.024) == "KB vs KiB"
    assert sub.diagnose(1000) == "kilo vs unit"
    assert sub.diagnose(7.3) is None
    assert sub.diagnose(1.5) is None
