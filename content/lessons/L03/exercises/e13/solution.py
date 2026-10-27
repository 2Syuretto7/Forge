def forward_accumulate(chain, x):
    """Return (value, derivative) by carrying the derivative forward."""
    v, d = x, 1.0
    for g, dg in chain:
        d = dg(v) * d
        v = g(v)
    return v, d


def stored_values(chain, x):
    """Inputs to each function in the chain, in order."""
    out = []
    v = x
    for g, _ in chain:
        out.append(v)
        v = g(v)
    return out


def reverse_accumulate(chain, x):
    """Return (value, derivative) via a forward pass then a backward pass."""
    saved = stored_values(chain, x)
    v = x
    for g, _ in chain:
        v = g(v)
    d = 1.0
    for (g, dg), inp in zip(reversed(chain), reversed(saved)):
        d = d * dg(inp)
    return v, d
