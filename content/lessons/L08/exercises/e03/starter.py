def transactions(stride, n_threads=32, elem_bytes=4, segment=32):
    """Thread t of a warp loads the element at byte address t * stride * elem_bytes. Count the distinct
    aligned memory segments of `segment` bytes the warp touches."""
    raise NotImplementedError


def efficiency(stride, n_threads=32, elem_bytes=4, segment=32):
    """Useful bytes divided by bytes transferred."""
    raise NotImplementedError
