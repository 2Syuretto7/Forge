import math
import re
import sub

KNOTS = sub.build_all(sub.TARGETS)


def test_max_gap():
    assert sub.max_gap(lambda x: 3 * x, 0, 1) == 0
    assert abs(sub.max_gap(lambda x: x * x, 0, 1, m=101) - 0.25) < 1e-12


def test_to_relus_reproduces_corners():
    f = math.sqrt
    knots = [0, 0.25, 1, 4]
    desc = sub.to_relus(f, knots)
    for t in knots:
        assert abs(sub.evaluate(desc, t) - f(t)) < 1e-12


def test_every_drawing_is_within_budget():
    for name, (f, a, b, tol) in sub.TARGETS.items():
        desc = sub.to_relus(f, KNOTS[name])
        worst = max(abs(sub.evaluate(desc, a + (b - a) * i / 4000) - f(a + (b - a) * i / 4000)) for i in range(4001))
        assert worst <= tol * 1.05 + 1e-12, f"{name}: error {worst:.4g} over budget {tol}"


def test_total_pieces():
    total = sum(len(k) - 1 for k in KNOTS.values())
    assert total <= 120, f"{total} pieces; the budget is 120"


def test_report_gives_each_count():
    for name, knots in KNOTS.items():
        m = re.search(rf"{name}\D*(\d+)", sub.REPORT)
        assert m, f"the report should mention {name} and its count"
        assert int(m.group(1)) == len(knots) - 1, f"{name}: report says {m.group(1)}, drawing has {len(knots) - 1} pieces"
