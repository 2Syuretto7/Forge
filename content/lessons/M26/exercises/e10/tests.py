import sub

S = sub.stream_sums()
E = sub.errors(S)


def test_truth():
    assert abs(S["exact"] - 5e7) < 2e4


def test_stalls():
    assert S["float16"] == 2048.0
    assert abs(S["float32"] - 2**24) < 1e5, S["float32"]


def test_good_methods():
    assert E["float64"] < 1e-6
    assert E["kahan32"] < 8 and E["pairwise32"] < 8, E
    assert set(E) == {"float16", "float32", "float64", "pairwise32", "kahan32"}
