import sub


def test_billion_embeddings():
    assert sub.index_bytes(10 ** 9, 768) == 3072 * 10 ** 9
    assert abs(sub.query_seconds(10 ** 9, 768, 1e14) - 0.01536) < 1e-12
    assert abs(sub.queries_per_second(10 ** 9, 768, 1e14) - 1 / 0.01536) < 1e-9


def test_capacity():
    assert sub.max_vectors(80 * 2 ** 30, 768, 2) == 55924053
