import numpy as np
import sub

# minimize (x - 2)^2 + (y - 1)^2 subject to x + y <= 2 and -x <= 0: optimum (1.5, 0.5), lambda = (1, 0)
X = np.array([1.5, 0.5])
GF = 2 * (X - np.array([2.0, 1.0]))
GG = np.array([[1.0, 1.0], [-1.0, 0.0]])
GV = np.array([X.sum() - 2, -X[0]])


def test_optimal_point():
    res = sub.kkt_residuals(GF, GG, GV, np.array([1.0, 0.0]))
    assert sub.is_kkt(res), res


def test_wrong_multiplier_on_an_inactive_constraint():
    res = sub.kkt_residuals(GF, GG, GV, np.array([1.0, 0.3]))
    assert res["slackness"] > 0.4 and res["stationarity"] > 0.2
    assert not sub.is_kkt(res)


def test_infeasible_point():
    x = np.array([2.0, 1.0])
    res = sub.kkt_residuals(2 * (x - np.array([2.0, 1.0])), GG, np.array([x.sum() - 2, -x[0]]), np.zeros(2))
    assert res["primal"] == 1.0 and res["stationarity"] == 0.0
