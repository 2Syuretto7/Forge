import sub

DIST_L = ("*", "a", ("+", "b", "c"))
DIST_R = ("+", ("*", "a", "b"), ("*", "a", "c"))
SQ = ("^", ("+", "a", "b"), 2)
WRONG = ("+", ("^", "a", 2), ("^", "b", 2))
RIGHT = ("+", ("+", ("^", "a", 2), ("*", ("*", 2, "a"), "b")), ("^", "b", 2))


def test_true_identities():
    assert sub.same_function(DIST_L, DIST_R, ["a", "b", "c"])
    assert sub.same_function(SQ, RIGHT, ["a", "b"])


def test_false_identities():
    assert not sub.same_function(SQ, WRONG, ["a", "b"])
    pt = sub.counterexample(SQ, WRONG, ["a", "b"])
    assert pt is not None and set(pt) == {"a", "b"}
    assert abs(sub.evaluate(SQ, pt) - sub.evaluate(WRONG, pt)) > 1e-6


def test_domain_points_are_skipped():
    # x^2 / x equals x wherever it is defined; the point x = 0 is outside its domain.
    assert sub.same_function(("/", ("^", "x", 2), "x"), "x", ["x"])


def test_invariant_self_agreement():
    for e in [DIST_L, DIST_R, SQ, WRONG, ("/", 1, ("-", "x", "y"))]:
        names = sorted({t for t in str(e) if t.isalpha()})
        assert sub.same_function(e, e, names)
    assert sub.counterexample(DIST_L, DIST_R, ["a", "b", "c"]) is None
