import math


def compute_budget(peak_flops, utilization, hours):
    """Floating-point operations available: peak rate times utilization times seconds."""
    return peak_flops * utilization * hours * 3600


def chinchilla_split(C, tokens_per_param=20):
    """Parameters N and tokens D with C = 6 N D and D = tokens_per_param N. Return (N, D)."""
    N = math.sqrt(C / (6 * tokens_per_param))
    return N, tokens_per_param * N


def epochs(D, corpus_tokens):
    """How many passes over the corpus D training tokens take."""
    return D / corpus_tokens
