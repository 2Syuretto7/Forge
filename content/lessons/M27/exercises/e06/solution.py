import math


def bits_per_token(nats):
    return nats / math.log(2)


def perplexity(nats):
    return math.exp(nats)


def nats_from_perplexity(ppl):
    return math.log(ppl)


def geometric_mean_prob(nats):
    return math.exp(-nats)


def uniform_loss(K):
    return math.log(K)
