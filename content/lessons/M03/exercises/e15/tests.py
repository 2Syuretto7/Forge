import itertools
import sub


def test_counterexample():
    for n in [2, 3, 7]:
        rel = sub.swap_counterexample(n)
        assert all(0 <= x < n and 0 <= y < n for x, y in rel)
        assert sub.forall_exists(rel, n) and not sub.exists_forall(rel, n)


def test_smallest_by_brute_force():
    assert sub.smallest_counterexample() == 2
    # On one element no relation separates them: try all of them.
    for bits in itertools.product([False, True], repeat=1):
        rel = {(0, 0)} if bits[0] else set()
        assert sub.forall_exists(rel, 1) == sub.exists_forall(rel, 1)


def test_one_direction_always_holds():
    for bits in itertools.product([False, True], repeat=9):
        rel = {(x, y) for (x, y), b in zip(itertools.product(range(3), repeat=2), bits) if b}
        if sub.exists_forall(rel, 3):
            assert sub.forall_exists(rel, 3)
