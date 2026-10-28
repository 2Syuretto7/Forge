class DynamicLossScaler:
    """The scale PyTorch's GradScaler manages: on a step whose gradients contain inf or NaN, skip the
    step and multiply the scale by backoff; after `interval` consecutive good steps, multiply it by
    growth."""

    def __init__(self, scale=2.0 ** 16, growth=2.0, backoff=0.5, interval=2000):
        self.scale, self.growth, self.backoff, self.interval = scale, growth, backoff, interval
        self.good = 0

    def update(self, found_inf):
        """Record one step; return True if the optimizer should apply it."""
        if found_inf:
            self.scale *= self.backoff
            self.good = 0
            return False
        self.good += 1
        if self.good == self.interval:
            self.scale *= self.growth
            self.good = 0
        return True
