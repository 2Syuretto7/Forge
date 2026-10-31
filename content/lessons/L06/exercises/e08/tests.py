import numpy as np
import sub

Xte, yte = sub.make_digits(1000, 1)


def test_reproducible_and_warmup():
    _, a = sub.train(3, 16, "pre", 3e-3, 20)
    _, b = sub.train(3, 16, "pre", 3e-3, 20)
    assert len(a) == 20 and a == b
    _, c = sub.train(3, 16, "pre", 3e-3, 20, warmup=10)
    assert c[0] == a[0] and c[5] != a[5]


def test_depth_20_plain_versus_pre_norm():
    _, plain = sub.train(20, 32, "plain", 3e-3, 300)
    p, pre = sub.train(20, 32, "pre", 3e-3, 300)
    assert np.mean(plain[-30:]) > 0.9, np.mean(plain[-30:])
    assert np.mean(pre[-30:]) < 0.4, np.mean(pre[-30:])
    assert sub.evaluate(p, Xte, yte, 20, "pre") > 0.75
