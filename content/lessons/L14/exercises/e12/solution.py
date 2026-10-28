import numpy as np


def generate(P, start, n, T, rng):
    """Sample n tokens from a bigram table P (rows are next-token distributions) at temperature T,
    by rescaling log-probabilities: p_T proportional to P^(1/T)."""
    seq = [start]
    for _ in range(n):
        logp = np.log(P[seq[-1]]) / T
        logp -= logp.max()
        q = np.exp(logp)
        seq.append(int(rng.choice(len(q), p=q / q.sum())))
    return seq


def distinct_ratio(seq, n=3):
    """Distinct n-grams divided by total n-grams: low values mean repetition."""
    grams = [tuple(seq[i:i + n]) for i in range(len(seq) - n + 1)]
    return len(set(grams)) / len(grams)


def model_nll(seq, P):
    """Mean negative log-likelihood of a sequence under the untempered model."""
    return float(-np.mean([np.log(P[a, b]) for a, b in zip(seq, seq[1:])]))
