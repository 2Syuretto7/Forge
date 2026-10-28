import sub


def test_same_tokens():
    for prompt in ([1, 2, 3], [5], [0, 11, 4, 7]):
        assert sub.generate_cached(prompt, 12) == sub.generate_uncached(prompt, 12)


def test_output_is_not_trivial():
    out = sub.generate_uncached([1, 2, 3], 10)[3:]
    assert len(set(out)) >= 3
