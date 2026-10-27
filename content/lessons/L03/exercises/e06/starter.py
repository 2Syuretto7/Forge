import numpy as np


def forward(A, b, x):
    raise NotImplementedError


def jvp(A, b, x, v):
    raise NotImplementedError


def vjp(A, b, x, u):
    raise NotImplementedError


def full_jacobian(A, b, x):
    raise NotImplementedError
