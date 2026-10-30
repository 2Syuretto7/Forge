import cmath
import math

import numpy as np


def eig2_complex(A):
    """Eigenvalues of a 2 by 2 matrix as complex numbers."""
    (a, b), (c, d) = A
    tr, det = a + d, a * d - b * c
    s = cmath.sqrt(tr * tr - 4 * det)
    return (tr + s) / 2, (tr - s) / 2


def rotation_scale(A):
    """(r, theta in degrees) of a scaled rotation."""
    z = max(eig2_complex(A), key=lambda w: w.imag)
    return abs(z), math.degrees(cmath.phase(z))


def orbit_norms(A, x0, k):
    """|A^j x0| for j = 0..k."""
    x = np.asarray(x0, dtype=float)
    out = [float(np.linalg.norm(x))]
    for _ in range(k):
        x = A @ x
        out.append(float(np.linalg.norm(x)))
    return out
