import math


def compute_budget(peak_flops, utilization, hours):
    """Floating-point operations available: peak rate times utilization times seconds."""
    raise NotImplementedError


def chinchilla_split(C, tokens_per_param=20):
    """Parameters N and tokens D with C = 6 N D and D = tokens_per_param N. Return (N, D)."""
    raise NotImplementedError


def epochs(D, corpus_tokens):
    """How many passes over the corpus D training tokens take."""
    raise NotImplementedError
