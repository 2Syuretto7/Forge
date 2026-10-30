import itertools


def is_function(pairs, domain):
    """Each element of domain appears exactly once as an input, and nothing else does."""
    raise NotImplementedError


def apply(pairs, x):
    """The output paired with x."""
    raise NotImplementedError


def is_injective(pairs):
    """No two inputs share an output."""
    raise NotImplementedError


def is_surjective(pairs, codomain):
    """Every element of codomain is an output."""
    raise NotImplementedError


def compose(f, g):
    """First g, then f."""
    raise NotImplementedError


def all_functions(domain, codomain):
    """Every function from domain to codomain, as lists of pairs."""
    raise NotImplementedError
