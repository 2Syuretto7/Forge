import math


def lr_at(step, peak, warmup, total, floor=0.1):
    """Linear warmup to peak over the first warmup steps, then cosine decay from peak to
    floor * peak at step total."""
    raise NotImplementedError


def steps_for_tokens(tokens, batch, ctx):
    """Optimizer steps needed to see at least `tokens` tokens with batches of `batch` windows
    of `ctx` tokens."""
    raise NotImplementedError
