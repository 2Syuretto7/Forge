import numpy as np
import sub

N, SRC, DST = sub.make_web()
SCORES, STEPS, RES = sub.pagerank(N, SRC, DST)
G = sub.google_dense(N, SRC, DST)


def test_reference_ranking():
    lam, V = np.linalg.eig(G)
    v = np.real(V[:, np.argmax(np.real(lam))])
    ref = v / v.sum()
    assert np.isclose(SCORES.sum(), 1) and np.allclose(SCORES, ref, atol=1e-8)
    assert sub.top(SCORES) == [int(i) for i in np.argsort(-ref, kind="stable")[:10]]


def test_dense_matrix():
    assert np.allclose(G.sum(axis=0), 1)


def test_second_eigenvalue_and_steps():
    lam2 = sub.second_eigenvalue(G)
    assert abs(lam2 - 0.85) < 1e-6
    start = np.zeros(N)
    start[-1] = 1.0
    x, steps, res = sub.pagerank(N, SRC, DST, start=start)
    assert np.allclose(x, SCORES, atol=1e-8)
    r = np.array(res[len(res) // 2:])
    assert abs(np.median(r[1:] / r[:-1]) - lam2) < 0.01, "the residual should shrink by |lambda_2| per step"
    pred = sub.predicted_steps(lam2, 1e-10, res[0])
    assert abs(steps - pred) <= 0.2 * pred, (steps, pred)
    assert STEPS < 0.5 * pred, "from the uniform start the slow mode is absent"
