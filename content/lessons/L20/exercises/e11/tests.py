import numpy as np
import sub

rng = np.random.default_rng(6)
V = 20


def make(prompt_len, n=300):
    tokens, mask = [], []
    for _ in range(n):
        tokens += rng.integers(0, 10, prompt_len).tolist() + rng.integers(10, 20, 5).tolist()
        mask += [0] * prompt_len + [1] * 5
    return np.array(tokens), np.array(mask)


def test_masking_matters_more_with_long_prompts():
    gaps = []
    for L in [5, 50]:
        t, m = make(L)
        masked = sub.response_ce(sub.fit_unigram(t, m, V), t, m)
        unmasked = sub.response_ce(sub.fit_unigram(t, np.ones_like(m), V), t, m)
        assert masked < unmasked
        gaps.append(unmasked - masked)
    assert gaps[1] > gaps[0] + 1.0
