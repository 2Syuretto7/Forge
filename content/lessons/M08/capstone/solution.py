import math
import random
from fractions import Fraction

C = math.comb

PUZZLES = {
    "sum_seven": "two dice sum to 7",
    "six_in_four": "at least one six in four rolls",
    "double_six_24": "at least one double six in 24 rolls of two dice",
    "birthday_23": "a shared birthday among 23 people",
    "two_aces": "two aces in two cards drawn from a deck",
    "full_house": "a full house in a 5-card hand",
    "three_heads": "at least three heads in a row in 10 flips",
    "derangement_10": "nobody of ten gets their own hat",
    "committee": "a committee of 3 of 10 includes Ada",
    "same_suit_3": "three cards all of one suit",
}

DECK = [(r, s) for r in range(13) for s in range(4)]


def _no_run_of_three(n):
    a = [1, 2, 4]
    while len(a) <= n:
        a.append(a[-1] + a[-2] + a[-3])
    return a[n]


def _derangements(n):
    d = [1, 0]
    for k in range(2, n + 1):
        d.append((k - 1) * (d[-1] + d[-2]))
    return d[n]


def _birthday(m):
    p = Fraction(1)
    for i in range(m):
        p *= Fraction(365 - i, 365)
    return 1 - p


EXACT = {
    "sum_seven": Fraction(1, 6),
    "six_in_four": 1 - Fraction(5, 6) ** 4,
    "double_six_24": 1 - Fraction(35, 36) ** 24,
    "birthday_23": _birthday(23),
    "two_aces": Fraction(C(4, 2), C(52, 2)),
    "full_house": Fraction(13 * C(4, 3) * 12 * C(4, 2), C(52, 5)),
    "three_heads": 1 - Fraction(_no_run_of_three(10), 2 ** 10),
    "derangement_10": Fraction(_derangements(10), math.factorial(10)),
    "committee": Fraction(C(9, 2), C(10, 3)),
    "same_suit_3": Fraction(4 * C(13, 3), C(52, 3)),
}


def _full_house(rng):
    hand = rng.sample(DECK, 5)
    ranks = sorted(sum(1 for c in hand if c[0] == r) for r in range(13))
    return ranks[-2:] == [2, 3]


TRIALS = {
    "sum_seven": lambda rng: rng.randint(1, 6) + rng.randint(1, 6) == 7,
    "six_in_four": lambda rng: any(rng.randint(1, 6) == 6 for _ in range(4)),
    "double_six_24": lambda rng: any(rng.randint(1, 6) == 6 and rng.randint(1, 6) == 6 for _ in range(24)),
    "birthday_23": lambda rng: len({rng.randrange(365) for _ in range(23)}) < 23,
    "two_aces": lambda rng: all(c[0] == 0 for c in rng.sample(DECK, 2)),
    "full_house": _full_house,
    "three_heads": lambda rng: "HHH" in "".join(rng.choice("HT") for _ in range(10)),
    "derangement_10": lambda rng: all(i != h for i, h in enumerate(rng.sample(range(10), 10))),
    "committee": lambda rng: 0 in rng.sample(range(10), 3),
    "same_suit_3": lambda rng: len({c[1] for c in rng.sample(DECK, 3)}) == 1,
}


def report(n, seed=0):
    """Exact, estimate, standard error and z for each puzzle."""
    rng = random.Random(seed)
    out = []
    for name in PUZZLES:
        p = float(EXACT[name])
        est = sum(1 for _ in range(n) if TRIALS[name](rng)) / n
        se = math.sqrt(p * (1 - p) / n)
        out.append({"name": name, "exact": p, "estimate": est, "se": se, "z": (est - p) / se})
    return out


def hash_plan(n_docs, risk):
    """Shortest hash with expected colliding pairs <= risk, and pairs expected at 64 bits."""
    pairs = C(n_docs, 2)
    bits = 0
    while pairs / 2 ** bits > risk:
        bits += 1
    return {"bits": bits, "expected_pairs_64": pairs / 2 ** 64}
