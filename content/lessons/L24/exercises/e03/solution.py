import math


def lr_at(step, peak, warmup, total, floor=0.1):
    """Linear warmup to peak over the first warmup steps, then cosine decay from peak to
    floor * peak at step total."""
    if step <= warmup:
        return peak * step / warmup
    progress = (step - warmup) / (total - warmup)
    return peak * (floor + (1 - floor) * 0.5 * (1 + math.cos(math.pi * progress)))


def steps_for_tokens(tokens, batch, ctx):
    """Optimizer steps needed to see at least `tokens` tokens with batches of `batch` windows
    of `ctx` tokens."""
    return math.ceil(tokens / (batch * ctx))
