import sub

P, W = 8.1e12, 320e9


def test_profiles():
    assert sub.profile("add", 1000) == (1000, 12000)
    assert sub.profile("matmul", 2, 3, 4) == (48, (8 + 12 + 6) * 4)
    assert sub.profile("softmax", 10, 20) == (1000, 1600)
    assert sub.profile("layernorm", 10, 20) == (1600, (400 + 40) * 4)


def test_placements():
    kinds = [("add", (1 << 24,)), ("softmax", (4096, 4096)), ("layernorm", (4096, 4096)), ("matvec", (4096, 4096)), ("matmul", (4096, 4096, 4096))]
    bounds = [sub.place(n, d, P, W)["bound"] for n, d in kinds]
    assert bounds == ["memory"] * 4 + ["compute"]
    mv = sub.place("matvec", (4096, 4096), P, W)
    mm = sub.place("matmul", (4096, 4096, 4096), P, W)
    per_flop_mv = mv["time"] / (2 * 4096 * 4096)
    per_flop_mm = mm["time"] / (2 * 4096**3)
    assert per_flop_mv / per_flop_mm > 50
