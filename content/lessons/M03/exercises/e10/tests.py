import sub

RESULTS = sub.run_hunter(sub.CLAIMS, 60)


def test_shape():
    assert len(sub.CLAIMS) == 50
    assert set(RESULTS) == {c["name"] for c in sub.CLAIMS}
    for name, (ce, tried) in RESULTS.items():
        assert 1 <= tried <= 60


def test_two_false_claims_survive_sixty_tries():
    false_names = sorted(c["name"] for c in sub.CLAIMS[:25])
    hidden = ["n < 100", "n divides 2^n - 2 only for prime n"]
    assert sub.broken(RESULTS) == sorted(n for n in false_names if n not in hidden)
    assert sub.survivors(RESULTS) == sorted([c["name"] for c in sub.CLAIMS[25:]] + hidden)


def test_a_longer_hunt_breaks_them_and_no_true_claim():
    longer = sub.run_hunter(sub.CLAIMS, 400)
    assert sub.broken(longer) == sorted(c["name"] for c in sub.CLAIMS[:25])
    assert longer["n divides 2^n - 2 only for prime n"][0] == 341


def test_some_counterexamples():
    assert RESULTS["n^2 + n + 41 is prime"] == (40, 41)
    assert RESULTS["2^(2^n) + 1 is prime"] == (5, 6)
    assert RESULTS["every prime is odd"] == (2, 1)
    assert RESULTS["2^n - 1 is prime for prime n"][0] == 11
