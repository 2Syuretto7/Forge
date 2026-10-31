WORD = 4


def profile(name, *dims):
    """(flops, bytes) of a kernel under the stated conventions."""
    if name == "add":
        (n,) = dims
        return n, 3 * n * WORD
    if name == "matvec":
        m, n = dims
        return 2 * m * n, (m * n + n + m) * WORD
    if name == "matmul":
        m, n, k = dims
        return 2 * m * n * k, (m * k + k * n + m * n) * WORD
    if name == "softmax":
        r, c = dims
        return 5 * r * c, 2 * r * c * WORD
    if name == "layernorm":
        r, c = dims
        return 8 * r * c, (2 * r * c + 2 * c) * WORD
    raise ValueError(name)


def place(name, dims, peak, bw):
    """Roofline placement of a kernel."""
    flops, nbytes = profile(name, *dims)
    I = flops / nbytes
    return {
        "intensity": I,
        "attainable": min(peak, I * bw),
        "bound": "memory" if I < peak / bw else "compute",
        "time": max(flops / peak, nbytes / bw),
    }
