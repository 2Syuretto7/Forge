import sub


def test_diagnoses():
    d = {name: sub.diagnose(f, F) for name, (f, F) in sub.CLAIMS.items()}
    assert d == {
        "sum of k": "proved",
        "sum of k, off by one": "no base",
        "sum of k^2 is n^2": "no step",
        "sum of odds is n^2 + n - 1": "no step",
    }


def test_claims():
    for name, (f, F) in sub.CLAIMS.items():
        assert sub.claim_ok(f, F) == (name == "sum of k")


def test_a_step_without_a_base_proves_nothing():
    f, F = sub.CLAIMS["sum of k, off by one"]
    assert sub.step_ok(f, F, 200) and not sub.claim_ok(f, F, 200)
