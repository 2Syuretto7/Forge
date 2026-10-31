import sub


def reference(vocab, ctx, d, n_layer):
    shapes = []
    for _ in range(n_layer):
        shapes += [(d,), (d,), (d, 3 * d), (3 * d,), (d, d), (d,), (d,), (d,), (d, 4 * d), (4 * d,), (4 * d, d), (d,)]
    shapes += [(d,), (d,)]
    count = 0
    for s in shapes:
        n = 1
        for v in s:
            n *= v
        count += n
    return count, count + vocab * d + ctx * d


def test_counts_match_the_architecture():
    for args in [(512, 128, 192, 4), (65, 128, 64, 2), (50257, 1024, 768, 12)]:
        out = sub.count_params(*args)
        non, total = reference(*args)
        assert out["non_embedding"] == non and out["total"] == total
        assert out["approx"] == 12 * args[3] * args[2] ** 2


def test_rule_of_thumb_improves_with_width():
    small = sub.count_params(65, 128, 64, 2)
    large = sub.count_params(50257, 2048, 4096, 32)
    assert abs(small["approx"] / small["non_embedding"] - 1) > 0.01
    assert abs(large["approx"] / large["non_embedding"] - 1) < 0.001
