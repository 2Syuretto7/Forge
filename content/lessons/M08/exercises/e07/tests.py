import math
import sub


def test_exact():
    assert abs(sub.p_shared(23) - 0.5072972343239854) < 1e-12
    assert sub.smallest_room(0.5) == 23
    assert sub.smallest_room(0.99) == 57


def test_approximation():
    for m in [10, 23, 40]:
        assert abs(sub.p_shared(m) - sub.p_shared_approx(m)) < 0.01


def test_simulation():
    est = sub.simulate_room(23, 4000)
    se = math.sqrt(0.507 * 0.493 / 4000)
    assert abs(est - sub.p_shared(23)) < 4 * se
