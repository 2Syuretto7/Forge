import random
import sub

rnd = random.Random(0)
CASES = {
    "even_sum": [(rnd.randint(-500, 500), rnd.randint(-500, 500)) for _ in range(500)],
    "square_even": list(range(-500, 501)),
    "root2": list(range(1, 300)),
    "cube_minus": list(range(-500, 501)),
    "odd_product": [(rnd.randint(-500, 500), rnd.randint(-500, 500)) for _ in range(500)],
    "new_prime": list(range(1, 13)),
    "odd_sum": list(range(0, 300)),
    "distributive": [tuple(set(rnd.sample(range(12), rnd.randint(0, 8))) for _ in range(3)) for _ in range(300)],
    "de_morgan": [{x: rnd.random() < 0.9 for x in range(10)} for _ in range(300)],
    "triangle": [(rnd.uniform(-100, 100), rnd.uniform(-100, 100)) for _ in range(500)],
}


def test_every_statement_has_a_predicate_proof_and_method():
    for name in sub.STATEMENTS:
        assert callable(sub.PREDICATES.get(name)), f"{name}: no predicate"
        assert sub.METHODS.get(name) in ("direct", "contrapositive", "contradiction", "cases"), f"{name}: bad method"
        words = len(str(sub.PROOFS.get(name) or "").split())
        assert words >= 40, f"{name}: the proof has {words} words; write at least 40"


def test_stress():
    assert sub.stress(lambda n: n < 3, range(10)) == 3
    assert sub.stress(lambda n: True, range(10)) is None


def test_no_counterexamples():
    for name, cases in CASES.items():
        assert sub.stress(sub.PREDICATES[name], cases) is None, f"{name} failed its stress test"


def test_a_false_variant_is_caught():
    # The same hunt refutes a slightly stronger claim: n^3 - n is not always divisible by 12.
    assert sub.stress(lambda n: (n ** 3 - n) % 12 == 0, CASES["cube_minus"]) is not None
