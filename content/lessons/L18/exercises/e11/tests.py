import sub


def test_finds_the_bug():
    assert sub.first_divergence([1, 2, 3], 10, sub.generate_cached_buggy) == 1


def test_correct_generator_passes():
    def reference(prompt, n):
        ids = list(prompt)
        for _ in range(n):
            ids.append(int(sub.logits_full(ids)[-1].argmax()))
        return ids
    assert sub.first_divergence([1, 2, 3], 10, reference) is None
