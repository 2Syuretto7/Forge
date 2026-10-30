import random
import sub


def test_divisible():
    assert sub.count_divisible(100, [2, 3]) == 67
    assert sub.count_divisible(1000, [2, 3, 5]) == sum(1 for k in range(1, 1001) if k % 2 == 0 or k % 3 == 0 or k % 5 == 0)


def test_invariant_matches_python_union():
    rnd = random.Random(0)
    for _ in range(300):
        sets = [set(rnd.sample(range(30), rnd.randint(0, 12))) for _ in range(rnd.randint(1, 5))]
        assert sub.union_size(sets) == len(set().union(*sets))
