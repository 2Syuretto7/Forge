import sub


def test_formulas_match_the_counters():
    for name, algo in sub.ALGORITHMS.items():
        sizes = range(8, 65, 8) if name == "matmul_blocked" else range(1, 41)
        for n in sizes:
            c = algo(n)
            assert c["ops"] == sub.FORMULAS[name](n), f"{name} at n = {n}: counted {c['ops']}"
            if name in sub.LOAD_FORMULAS:
                assert c["loads"] == sub.LOAD_FORMULAS[name](n), f"{name} loads at n = {n}"


def test_induction():
    for name, F in sub.FORMULAS.items():
        if name == "matmul_blocked":
            assert F(8) == sub.ALGORITHMS[name](8)["ops"]
            for n in range(8, 200, 8):
                assert F(n + 8) - F(n) == sub.STEPS[name](n), f"{name}: step from {n}"
            continue
        assert F(1) == sub.ALGORITHMS[name](1)["ops"], f"{name}: base case"
        for n in range(1, 61):
            assert F(n + 1) - F(n) == sub.STEPS[name](n), f"{name}: step from {n} to {n + 1}"


def test_doubling_ratios():
    for name, algo in sub.ALGORITHMS.items():
        counted = algo(128)["ops"] / algo(64)["ops"]
        predicted = sub.predicted_ratio(name, 64)
        assert abs(counted / predicted - 1) <= 0.2, f"{name}: counted {counted:.3f}, predicted {predicted:.3f}"


def test_blocking_cuts_loads():
    assert sub.ALGORITHMS["matmul_naive"](64)["loads"] == 8 * sub.ALGORITHMS["matmul_blocked"](64)["loads"]
