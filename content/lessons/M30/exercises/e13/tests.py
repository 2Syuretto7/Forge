import sub


def test_diagnosis():
    d = {name: sub.diagnose(*cand) for name, cand in sub.CANDIDATES.items()}
    assert d["solver_a"] == "optimal"
    assert d["solver_b"] in ("slackness", "stationarity")
    assert sub.residuals(*sub.CANDIDATES["solver_b"])["slackness"] > 0.5
    assert d["solver_c"] == "primal"
