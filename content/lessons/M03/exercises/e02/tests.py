import random
import sub


def test_classic_equivalences():
    contra = lambda p, q: (not (not q)) or (not p)  # (not q) implies (not p)
    assert sub.equivalent(lambda p, q: (not p) or q, contra, 2)
    assert not sub.equivalent(lambda p, q: (not p) or q, lambda p, q: (not q) or p, 2)
    assert sub.counterexamples(lambda p, q: (not p) or q, lambda p, q: (not q) or p, 2) == [(True, False), (False, True)]


def test_tautology_and_satisfiable():
    assert sub.tautology(lambda p: p or not p, 1)
    assert not sub.satisfiable(lambda p: p and not p, 1)
    assert sub.satisfiable(lambda p, q: p and not q, 2) and not sub.tautology(lambda p, q: p and not q, 2)


def random_formula(rnd, n, d):
    if d == 0 or rnd.random() < 0.3:
        i = rnd.randrange(n)
        return lambda *x, i=i: x[i]
    a, b = random_formula(rnd, n, d - 1), random_formula(rnd, n, d - 1)
    k = rnd.choice(["and", "or", "not"])
    if k == "and":
        return lambda *x: a(*x) and b(*x)
    if k == "or":
        return lambda *x: a(*x) or b(*x)
    return lambda *x: not a(*x)


def test_invariant_de_morgan_on_random_formulas():
    rnd = random.Random(0)
    for _ in range(300):
        f, g = random_formula(rnd, 3, 3), random_formula(rnd, 3, 3)
        assert sub.equivalent(lambda *x: not (f(*x) and g(*x)), lambda *x: (not f(*x)) or (not g(*x)), 3)
        assert sub.equivalent(f, f, 3)
        assert sub.satisfiable(f, 3) == (not sub.tautology(lambda *x: not f(*x), 3))
