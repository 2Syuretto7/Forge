def product_rule(f, df, g, dg):
    """(f g)'."""
    return lambda x: df(x) * g(x) + f(x) * dg(x)


def quotient_rule(f, df, g, dg):
    """(f / g)'."""
    return lambda x: (df(x) * g(x) - f(x) * dg(x)) / g(x) ** 2


def chain_rule(f, df, g, dg):
    """(f o g)'."""
    def d(x):
        u = g(x)
        return df(u) * dg(x)
    return d
