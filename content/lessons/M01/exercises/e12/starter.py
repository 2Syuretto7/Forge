def weight_bytes(n_params, bytes_per_param=2):
    """Bytes to store the weights."""
    raise NotImplementedError


def adam_bytes(n_params):
    """Bytes to train with Adam in mixed precision: 16 per parameter."""
    raise NotImplementedError


def to_gib(n_bytes):
    """Bytes to GiB (2**30 bytes)."""
    raise NotImplementedError


def max_params(gib, bytes_per_param):
    """Largest whole number of parameters fitting in gib GiB."""
    raise NotImplementedError
