def weight_bytes(n_params, bytes_per_param=2):
    """Bytes to store the weights."""
    return n_params * bytes_per_param


def adam_bytes(n_params):
    """Bytes to train with Adam in mixed precision: 16 per parameter."""
    return n_params * (2 + 2 + 4 + 4 + 4)


def to_gib(n_bytes):
    """Bytes to GiB (2**30 bytes)."""
    return n_bytes / 2 ** 30


def max_params(gib, bytes_per_param):
    """Largest whole number of parameters fitting in gib GiB."""
    return int(gib * 2 ** 30) // bytes_per_param
