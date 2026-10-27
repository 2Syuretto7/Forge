import numpy as np
import sub

rng = np.random.default_rng(10)


def _loss(sizes, B, seed=0):
    m = sub.MLP(sizes, seed)
    X = rng.normal(size=(B, sizes[0]))
    y = rng.integers(0, sizes[-1], size=B)
    return sub.cross_entropy_fused(m(sub.Tensor(X)), y)


def test_graph_nodes():
    a = sub.Tensor(np.ones(3))
    b = a * a
    c = (b + a).sum()
    nodes = sub.graph_nodes(c)
    assert len(nodes) == 4 and len({id(n) for n in nodes}) == 4
    assert any(n is a for n in nodes)


def test_saved_bytes_matches_formula():
    for sizes, B in [([4, 8, 3], 5), ([6, 16, 16, 4], 7), ([3, 2], 11)]:
        assert sub.saved_bytes(_loss(sizes, B)) == sub.mlp_saved_bytes_formula(sizes, B), sizes


def test_formula_by_hand():
    assert sub.mlp_saved_bytes_formula([512, 512, 512, 10], 1) == 8 * (3 * 512 + 512 * 512 * 2 + 512 * 10 + 2 * 512 + 10)


def test_activations_scale_with_batch():
    sizes = [32, 64, 64, 10]
    a = sub.mlp_saved_bytes_formula(sizes, 100)
    b = sub.mlp_saved_bytes_formula(sizes, 200)
    weights = 8 * sum(i * o for i, o in zip(sizes, sizes[1:]))
    assert b - a == a - weights
