import numpy as np


def static_batching(requests, batch_size):
    """requests: list of (arrival_step, output_tokens), sorted by arrival. A batch starts when the
    server is free and takes up to batch_size waiting requests (waiting until at least one has
    arrived); it runs until its longest request finishes, one token per step. Return each
    request's finish step (in request order)."""
    raise NotImplementedError


def continuous_batching(requests, batch_size):
    """Iteration-level scheduling: at every step, fill free slots with waiting requests, then every
    running request produces one token; a request leaves as soon as it has all its tokens. Return
    each request's finish step."""
    raise NotImplementedError
