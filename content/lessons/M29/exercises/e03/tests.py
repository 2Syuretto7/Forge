import numpy as np
import sub

D = np.diag(np.geomspace(1, 100, 10))
B = np.ones(10)
X0 = np.zeros(10)


def test_rate():
    a, b = sub.optimal_heavy_ball(100.0, 1.0)
    assert abs(b - (9 / 11) ** 2) < 1e-12
    e = sub.heavy_ball(D, B, X0, a, b, 400)
    k = np.arange(60, 140)
    rho = np.exp(np.polyfit(k, np.log(e[60:140]), 1)[0])
    assert abs(rho - 9 / 11) < 0.015, rho
    assert e[150] < 1e-9 * e[0]


def test_ten_times_fewer_steps_than_gd():
    a, b = sub.optimal_heavy_ball(100.0, 1.0)
    e_hb = sub.heavy_ball(D, B, X0, a, b, 2000)
    e_gd = sub.heavy_ball(D, B, X0, 2 / 101, 0.0, 2000)
    k_hb = int(np.argmax(e_hb < 1e-6 * e_hb[0]))
    k_gd = int(np.argmax(e_gd < 1e-6 * e_gd[0]))
    assert 6 < k_gd / k_hb < 12, (k_gd, k_hb)
