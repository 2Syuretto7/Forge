import math
import random
import sub


def test_conversions():
    x = [1.0, 2.0, 3.0, 4.0]
    assert sub.to_complex(x) == [1 + 2j, 3 + 4j]
    assert sub.from_complex(sub.to_complex(x)) == x


def test_encode_preserves_length():
    rnd = random.Random(0)
    x = [rnd.gauss(0, 1) for _ in range(16)]
    y = sub.encode(x, 123)
    assert abs(math.fsum(v * v for v in y) - math.fsum(v * v for v in x)) < 1e-12
    assert sub.encode(x, 0) == x or max(abs(a - b) for a, b in zip(sub.encode(x, 0), x)) < 1e-15


def test_shift_invariance():
    rnd = random.Random(1)
    q = [rnd.gauss(0, 1) for _ in range(8)]
    k = [rnd.gauss(0, 1) for _ in range(8)]
    assert abs(sub.score(q, k, 10, 3) - sub.score(q, k, 1010, 1003)) < 1e-9
    assert abs(sub.score(q, k, 10, 3) - sub.score_from_offset(q, k, 7)) < 1e-9


def test_thousand_pairs():
    assert sub.verify(1000, 64) < 1e-9


def test_proof():
    words = sub.PROOF.split()
    assert len(words) >= 60, f"{len(words)} words; write at least 60"
    assert "conjugate" in sub.PROOF.lower()
