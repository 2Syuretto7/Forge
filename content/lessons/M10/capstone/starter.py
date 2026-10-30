from functools import reduce

import numpy as np

# provided
F = np.array([[0, 0], [0.6, 0], [0.6, 1.2], [1.4, 1.2], [1.4, 1.6], [0.6, 1.6], [0.6, 2.2], [1.8, 2.2], [1.8, 2.6], [0, 2.6]])

# provided
TARGETS = [
    ("rotate 90 degrees counterclockwise", [(0.0, 0.0), (0.0, 0.6), (-1.2, 0.6), (-1.2, 1.4), (-1.6, 1.4), (-1.6, 0.6), (-2.2, 0.6), (-2.2, 1.8), (-2.6, 1.8), (-2.6, 0.0)]),
    ("reflect across the x axis", [(0.0, 0.0), (0.6, 0.0), (0.6, -1.2), (1.4, -1.2), (1.4, -1.6), (0.6, -1.6), (0.6, -2.2), (1.8, -2.2), (1.8, -2.6), (0.0, -2.6)]),
    ("stretch x by 2 and squash y to half", [(0.0, 0.0), (1.2, 0.0), (1.2, 0.6), (2.8, 0.6), (2.8, 0.8), (1.2, 0.8), (1.2, 1.1), (3.6, 1.1), (3.6, 1.3), (0.0, 1.3)]),
    ("shear: each point moves right by its height", [(0.0, 0.0), (0.6, 0.0), (1.8, 1.2), (2.6, 1.2), (3.0, 1.6), (2.2, 1.6), (2.8, 2.2), (4.0, 2.2), (4.4, 2.6), (2.6, 2.6)]),
    ("rotate 45 degrees, then stretch x by 2", [(0.0, 0.0), (0.8485281374239, 0.4242640687119), (-0.8485281374239, 1.2727922061358), (0.2828427124746, 1.838477631085), (-0.2828427124746, 2.1213203435596), (-1.4142135623731, 1.5556349186104), (-2.262741699797, 1.9798989873223), (-0.5656854249492, 2.8284271247462), (-1.1313708498985, 3.1112698372208), (-3.67695526217, 1.838477631085)]),
    ("stretch x by 2, then rotate 45 degrees", [(0.0, 0.0), (0.8485281374239, 0.8485281374239), (0.0, 1.6970562748477), (1.1313708498985, 2.8284271247462), (0.8485281374239, 3.1112698372208), (-0.2828427124746, 1.9798989873223), (-0.7071067811865, 2.4041630560343), (0.9899494936612, 4.101219330882), (0.7071067811865, 4.3840620433566), (-1.838477631085, 1.838477631085)]),
    ("reflect across the line y = x", [(0.0, 0.0), (0.0, 0.6), (1.2, 0.6), (1.2, 1.4), (1.6, 1.4), (1.6, 0.6), (2.2, 0.6), (2.2, 1.8), (2.6, 1.8), (2.6, 0.0)]),
    ("shear by 0.5 along the line at 30 degrees: rotate by -30, shear x by 0.5, rotate back by 30", [(0.0, 0.0), (0.4700961894323, -0.075), (0.9200961894323, 1.3848076211353), (1.5468911086754, 1.2848076211353), (1.6968911086754, 1.7714101615138), (1.0700961894323, 1.8714101615138), (1.2950961894323, 2.6013139720814), (2.235288568297, 2.4513139720814), (2.385288568297, 2.9379165124599), (0.975, 3.1629165124599)]),
]


def rot(degrees):
    """Counterclockwise rotation."""
    raise NotImplementedError


def scale(sx, sy):
    """Stretch the axes."""
    raise NotImplementedError


def shear_x(k):
    """(x, y) -> (x + k y, y)."""
    raise NotImplementedError


def reflect_x():
    """Across the x axis."""
    raise NotImplementedError


def swap():
    """Across the line y = x."""
    raise NotImplementedError


def recipes():
    """For each target, the primitive matrices in the order applied."""
    raise NotImplementedError


def build(steps):
    """Matrix of the steps applied in order."""
    raise NotImplementedError


def fit_matrix(src, dst):
    """Least-squares M with dst rows close to M times src rows."""
    raise NotImplementedError


def report():
    """(max point error, max matrix difference from the fit, det) for each target."""
    raise NotImplementedError
