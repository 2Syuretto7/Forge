import numpy as np


def hessian_from_grad(grad, x, h=1e-5):
    raise NotImplementedError


def is_local_min(H, tol=1e-8):
    raise NotImplementedError


def curvature_bound(H):
    raise NotImplementedError
