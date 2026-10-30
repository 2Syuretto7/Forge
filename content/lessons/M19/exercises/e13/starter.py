def forward_accumulate(chain, x):
    """Return (value, derivative) by carrying the derivative forward."""
    raise NotImplementedError


def stored_values(chain, x):
    """Inputs to each function in the chain, in order."""
    raise NotImplementedError


def reverse_accumulate(chain, x):
    """Return (value, derivative) via a forward pass then a backward pass."""
    raise NotImplementedError
