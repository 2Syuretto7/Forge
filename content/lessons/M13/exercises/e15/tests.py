import math

import numpy as np
import sub


def rot(deg, r=1.0):
    t = math.radians(deg)
    return r * np.array([[math.cos(t), -math.sin(t)], [math.sin(t), math.cos(t)]])


def test_rotation():
    z1, z2 = sub.eig2_complex(rot(30))
    assert abs(z1 - complex(math.cos(math.radians(30)), math.sin(math.radians(30)))) < 1e-12
    assert abs(z2 - z1.conjugate()) < 1e-12


def test_spiral():
    r, th = sub.rotation_scale(rot(20, 1.1))
    assert abs(r - 1.1) < 1e-12 and abs(th - 20) < 1e-9
    n = sub.orbit_norms(rot(20, 1.1), [1.0, 0.0], 10)
    assert np.isclose(n[10], 1.1 ** 10)


def test_real_eigenvalues_still_work():
    z1, z2 = sub.eig2_complex(np.array([[2.0, 1], [1, 2]]))
    assert z1 == 3 and z2 == 1
