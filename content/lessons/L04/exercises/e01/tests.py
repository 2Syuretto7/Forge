import random
import sub

DIAMOND = {"x": [], "a": ["x"], "b": ["x"], "c": ["a", "b"], "L": ["c"], "w": []}


def _valid(parents, order):
    pos = {n: i for i, n in enumerate(order)}
    return sorted(order) == sorted(parents) and all(pos[p] < pos[n] for n in parents for p in parents[n])


def test_diamond():
    order = sub.topo_order(DIAMOND)
    assert _valid(DIAMOND, order), order


def test_random_dags():
    rnd = random.Random(0)
    for _ in range(30):
        n = rnd.randint(2, 25)
        names = [f"n{i}" for i in range(n)]
        rnd.shuffle(names)
        parents = {names[i]: [names[j] for j in range(i) if rnd.random() < 0.3] for i in range(n)}
        keys = list(parents)
        rnd.shuffle(keys)
        parents = {k: parents[k] for k in keys}
        assert _valid(parents, sub.topo_order(parents))


def test_cycle_raises():
    cyc = {"a": ["c"], "b": ["a"], "c": ["b"], "d": []}
    try:
        sub.topo_order(cyc)
    except ValueError:
        return
    raise AssertionError("no ValueError for a cycle")


def test_self_loop_raises():
    try:
        sub.topo_order({"a": ["a"]})
    except ValueError:
        return
    raise AssertionError("no ValueError for a self-loop")


def test_ancestors():
    assert sub.ancestors(DIAMOND, "L") == {"x", "a", "b", "c", "L"}
    assert sub.ancestors(DIAMOND, "a") == {"x", "a"}
    assert sub.ancestors(DIAMOND, "w") == {"w"}
