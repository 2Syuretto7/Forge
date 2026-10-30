import itertools


def is_function(pairs, domain):
    """Each element of domain appears exactly once as an input, and nothing else does."""
    inputs = [a for a, _ in pairs]
    return sorted(inputs, key=repr) == sorted(domain, key=repr) and len(set(inputs)) == len(inputs)


def apply(pairs, x):
    """The output paired with x."""
    for a, b in pairs:
        if a == x:
            return b
    raise KeyError(x)


def is_injective(pairs):
    """No two inputs share an output."""
    outs = [b for _, b in pairs]
    return len(set(outs)) == len(outs)


def is_surjective(pairs, codomain):
    """Every element of codomain is an output."""
    outs = {b for _, b in pairs}
    return all(c in outs for c in codomain)


def compose(f, g):
    """First g, then f."""
    return [(x, apply(f, y)) for x, y in g]


def all_functions(domain, codomain):
    """Every function from domain to codomain, as lists of pairs."""
    return [list(zip(domain, outs)) for outs in itertools.product(codomain, repeat=len(domain))]
