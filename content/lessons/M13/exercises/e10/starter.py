import numpy as np


def make_graph(n, k=10, seed=0):
    """(src, dst) of a random graph with popular low-numbered pages."""
    raise NotImplementedError


def step(src, dst, outdeg, x, d):
    """x -> G x without forming G."""
    raise NotImplementedError


def pagerank_sparse(src, dst, n, d=0.85, tol=1e-10, max_iter=1000):
    """(PageRank vector, residual per step)."""
    raise NotImplementedError
