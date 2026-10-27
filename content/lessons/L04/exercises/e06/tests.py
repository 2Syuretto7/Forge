import math
import sub


def test_puzzle_numbers():
    assert abs(sub.bits_per_token(1.5) - 2.1640425613334453) < 1e-12
    assert abs(sub.perplexity(1.5) - 4.4816890703380645) < 1e-12
    assert abs(sub.geometric_mean_prob(1.5) - 0.22313016014842982) < 1e-12


def test_round_trip_and_uniform():
    assert abs(sub.nats_from_perplexity(sub.perplexity(2.7)) - 2.7) < 1e-12
    assert abs(sub.uniform_loss(70) - math.log(70)) < 1e-12
    assert abs(sub.perplexity(sub.uniform_loss(50257)) - 50257) < 1e-6


def test_geometric_mean_from_a_sequence():
    probs = [0.5, 0.1, 0.8, 0.25]
    nats = -sum(math.log(p) for p in probs) / len(probs)
    gm = math.prod(probs) ** (1 / len(probs))
    assert abs(sub.geometric_mean_prob(nats) - gm) < 1e-12
