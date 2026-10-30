def square(x):
    """x squared."""
    return x * x


def relu(x):
    """max(0, x)."""
    return max(0, x)


def affine(a, b):
    """The machine x -> a x + b."""
    def machine(x):
        return a * x + b
    return machine


def apply_all(f, xs):
    """[f(x) for x in xs]."""
    return [f(x) for x in xs]
