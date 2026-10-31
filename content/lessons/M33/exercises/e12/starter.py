WORD = 4


def profile(name, *dims):
    """(flops, bytes) of a kernel under the stated conventions."""
    raise NotImplementedError


def place(name, dims, peak, bw):
    """Roofline placement of a kernel."""
    raise NotImplementedError
