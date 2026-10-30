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
    raise NotImplementedError


def _derangements(n):
    raise NotImplementedError


def _birthday(m):
    raise NotImplementedError


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
    raise NotImplementedError


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
    raise NotImplementedError


def hash_plan(n_docs, risk):
    """Shortest hash with expected colliding pairs <= risk, and pairs expected at 64 bits."""
    raise NotImplementedError
