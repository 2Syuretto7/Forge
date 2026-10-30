import math
import sub

ANGLES = [0, 30, 45, 90, 180, 270]


def test_sin_degrees():
    assert abs(sub.sin_degrees(30) - 0.5) < 1e-15
    assert abs(sub.sin_degrees(90) - 1) < 1e-15


def test_units_used():
    assert sub.units_used(ANGLES, [sub.sin_degrees(a) for a in ANGLES]) == "degrees"
    assert sub.units_used(ANGLES, [math.sin(a) for a in ANGLES]) == "radians"
    assert sub.units_used(ANGLES, [0.0] * 6) == "unknown"


def test_suspicious():
    assert sub.suspicious(ANGLES, [math.sin(a) for a in ANGLES])
    assert not sub.suspicious(ANGLES, [sub.sin_degrees(a) for a in ANGLES])
    assert not sub.suspicious([0], [math.sin(0)]), "0 is the same in both units"
