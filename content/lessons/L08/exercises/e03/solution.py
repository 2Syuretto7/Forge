def transactions(stride, n_threads=32, elem_bytes=4, segment=32):
    """Thread t of a warp loads the element at byte address t * stride * elem_bytes. Count the distinct
    aligned memory segments of `segment` bytes the warp touches."""
    return len({(t * stride * elem_bytes) // segment for t in range(n_threads)})


def efficiency(stride, n_threads=32, elem_bytes=4, segment=32):
    """Useful bytes divided by bytes transferred."""
    return n_threads * elem_bytes / (transactions(stride, n_threads, elem_bytes, segment) * segment)
