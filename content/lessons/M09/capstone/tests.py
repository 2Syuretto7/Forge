import numpy as np
import sub

X, Q = sub.make_corpus(0)
INDEX = sub.build(X)


def test_kmeans_shapes():
    C, a = sub.kmeans(X[:2000], 8, 3)
    assert C.shape == (8, 48) and a.shape == (2000,)
    assert np.allclose(np.linalg.norm(C, axis=1), 1)


def test_index_covers_every_row_once():
    rows = np.concatenate(INDEX["lists"])
    assert sorted(rows.tolist()) == list(range(len(X)))


def test_recall_and_cost():
    found, scanned = [], []
    for q in Q:
        f, n = sub.search(INDEX, X, q)
        found.append(f)
        scanned.append(n)
    exact = [sub.exact_search(X, q) for q in Q]
    r = sub.recall(found, exact)
    frac = np.mean(scanned) / len(X)
    assert r >= 0.9, f"recall@5 = {r:.2f}"
    assert frac <= 0.25, f"scanned {frac:.0%} of the database"


def test_recall_function():
    assert sub.recall([[1, 2, 3]], [[1, 2, 4]]) == 2 / 3
