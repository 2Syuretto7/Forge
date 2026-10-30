import math
import sub


def test_formulas():
    assert abs(sub.expected_colliding_pairs(10 ** 6, 32) - 116.41520541161299) < 1e-9
    assert sub.p_any_collision(10 ** 6, 32) > 0.999
    assert abs(sub.p_any_collision(65536, 32) - (1 - math.exp(-0.49999237060546875))) < 1e-12


def test_simulation_24_bits():
    exp = sub.expected_colliding_pairs(10 ** 5, 24)
    got = sub.simulated_colliding_pairs(10 ** 5, 24)
    assert abs(got - exp) < 4 * math.sqrt(exp), (got, exp)


def test_simulation_32_bits():
    got = sub.simulated_colliding_pairs(10 ** 5, 32)
    assert got <= 8
