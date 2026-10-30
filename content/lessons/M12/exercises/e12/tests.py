import numpy as np
import sub


def test_matches_full_fit():
    chunks = list(sub.make_chunks(3000, 4, 700, seed=1))
    A = np.vstack([a for a, _ in chunks])
    b = np.concatenate([v for _, v in chunks])
    ref, *_ = np.linalg.lstsq(A, b, rcond=None)
    assert np.allclose(sub.stream_fit(iter(chunks)), ref)


def test_million_rows():
    x = sub.stream_fit(sub.make_chunks(1_000_000, 5, 50_000))
    assert np.allclose(x, [1, 2, 3, 4, 5], atol=2e-3)
