import random
import sub

R = range(10)


def test_basic():
    assert sub.for_all(lambda x: x < 10, R) and not sub.for_all(lambda x: x < 9, R)
    assert sub.exists(lambda x: x == 3, R) and not sub.exists(lambda x: x > 20, R)
    assert sub.for_all(lambda x: False, []) and not sub.exists(lambda x: True, [])


def test_order_matters():
    succ = lambda x, y: y == (x + 1) % 10
    assert sub.for_all_exists(succ, R, R)
    assert not sub.exists_for_all(succ, R, R)
    assert sub.exists_for_all(lambda x, y: y >= x, R, R)


def test_invariant_negation_and_implication():
    rnd = random.Random(1)
    for _ in range(500):
        table = {x: rnd.random() < 0.8 for x in R}
        p = lambda x: table[x]
        assert (not sub.for_all(p, R)) == sub.exists(lambda x: not p(x), R)
        rel_t = {(x, y): rnd.random() < 0.5 for x in R for y in R}
        rel = lambda x, y: rel_t[(x, y)]
        if sub.exists_for_all(rel, R, R):
            assert sub.for_all_exists(rel, R, R)
