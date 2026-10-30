import random
import sub

Q = sub.Quantity


def test_speed():
    v = Q(180, {"km": 1}) / Q(3, {"h": 1})
    assert abs(v.value - 60) < 1e-12 and v.units == {"km": 1, "h": -1}
    d = v * Q(2, {"h": 1})
    assert abs(d.value - 120) < 1e-12 and d.units == {"km": 1}, "hours should cancel"


def test_plain_numbers_scale():
    q = Q(5, {"B": 1})
    assert (2 * q) == Q(10, {"B": 1})
    assert (q * 2) == Q(10, {"B": 1})
    assert (q / 5) == Q(1, {"B": 1})
    assert Q(3).units == {}


def test_refuses_to_add_different_units():
    assert (Q(1, {"m": 1}) + Q(2, {"m": 1})) == Q(3, {"m": 1})
    for op in ["add", "sub"]:
        try:
            if op == "add":
                Q(1, {"m": 1}) + Q(1, {"s": 1})
            else:
                Q(1, {"m": 1}) - Q(1, {"s": 1})
        except ValueError:
            continue
        raise AssertionError(f"{op} of metres and seconds should raise ValueError")


def test_zero_powers_are_dropped():
    q = Q(4, {"m": 1, "s": 0})
    assert q.units == {"m": 1}
    r = Q(6, {"FLOP": 1, "s": -1}) * Q(2, {"s": 1})
    assert r.units == {"FLOP": 1}


def test_invariant_multiply_then_divide():
    rnd = random.Random(0)
    names = ["m", "s", "kg", "B", "FLOP"]
    for _ in range(500):
        a = Q(rnd.uniform(0.1, 100), {n: rnd.randint(-2, 2) for n in rnd.sample(names, 2)})
        b = Q(rnd.uniform(0.1, 100), {n: rnd.randint(-2, 2) for n in rnd.sample(names, 3)})
        assert (a * b) / b == a, (a.units, b.units)
