import random
import sub


def test_against_python_sets():
    A, B = [1, 2, 3, 4], [3, 4, 5]
    assert set(sub.union(A, B)) == {1, 2, 3, 4, 5} and len(sub.union(A, B)) == 5
    assert set(sub.intersection(A, B)) == {3, 4}
    assert set(sub.difference(A, B)) == {1, 2}
    assert sub.is_subset([3, 4], A) and not sub.is_subset(B, A)
    assert set(sub.product([1, 2], ["a", "b"])) == {(1, "a"), (1, "b"), (2, "a"), (2, "b")}


def test_power_set():
    ps = sub.power_set([1, 2, 3])
    assert len(ps) == 8
    assert {frozenset(s) for s in ps} == {frozenset(s) for s in [[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]}


def test_invariant_counting():
    rnd = random.Random(2)
    for _ in range(300):
        A = rnd.sample(range(20), rnd.randint(0, 8))
        B = rnd.sample(range(20), rnd.randint(0, 8))
        assert len(sub.union(A, B)) == len(A) + len(B) - len(sub.intersection(A, B))
        assert len(sub.product(A, B)) == len(A) * len(B)
        assert sub.is_subset(sub.intersection(A, B), sub.union(A, B))
        if len(A) <= 6:
            assert len(sub.power_set(A)) == 2 ** len(A)
