def train_flops_per_token(n_params, n_layer, ctx, d):
    """Training FLOPs per token: 6 per parameter (2 forward, 4 backward) plus attention. In forward,
    each layer spends 2 ctx d on the scores q k^T and 2 ctx d on the weighted sum of values (masked
    entries included); backward costs twice the forward."""
    raise NotImplementedError


def attention_share(ctx, d):
    """Fraction of training FLOPs spent on attention scores and sums when N = 12 n_layer d^2."""
    raise NotImplementedError


def tokens_for_budget(C, n_params):
    """Tokens a budget of C FLOPs buys for a model of n_params parameters, with C = 6 N D."""
    raise NotImplementedError


def mfu(tokens_per_second, flops_per_token, peak_flops):
    """Model FLOPs utilization: the fraction of the hardware's peak the training run achieves."""
    raise NotImplementedError
