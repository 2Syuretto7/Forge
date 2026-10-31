import math
import sub


def _f_float(a, b, c):
    d = a * b + math.tanh(c)
    e = (d * a + 2.0) ** 2
    return math.exp(-e / 10.0) + 3.0 * a - b / (c * c + 1.0)


def _f_value(a, b, c):
    d = a * b + c.tanh()
    e = (d * a + 2.0) ** 2
    return (e * (-1.0 / 10.0)).exp() + 3 * a - b * (c * c + 1.0) ** -1


def test_forward():
    a, b, c = sub.Value(0.7), sub.Value(-1.3), sub.Value(0.4)
    assert abs(_f_value(a, b, c).data - _f_float(0.7, -1.3, 0.4)) < 1e-12


def test_grad_composite():
    x = [0.7, -1.3, 0.4]
    vs = [sub.Value(v) for v in x]
    _f_value(*vs).backward()
    for i in range(3):
        xp, xm = list(x), list(x)
        xp[i] += 1e-6
        xm[i] -= 1e-6
        num = (_f_float(*xp) - _f_float(*xm)) / 2e-6
        assert abs(vs[i].grad - num) < 1e-6 * max(1.0, abs(num)), (i, vs[i].grad, num)


def test_grad_reuse_accumulates():
    x = sub.Value(3.0)
    y = x * x + x
    y.backward()
    assert abs(x.grad - 7.0) < 1e-12


def test_numbers_on_both_sides():
    x = sub.Value(2.0)
    y = 2 * x + 1
    z = 1 + x * 3
    assert y.data == 5.0 and z.data == 7.0
    (y * z).backward()
    assert abs(x.grad - (2 * 7 + 5 * 3)) < 1e-12
