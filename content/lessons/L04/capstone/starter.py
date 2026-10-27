import heapq
import math
from collections import Counter

CORPUS = (
    "the old harbor town wakes before the sun. fishermen check their nets by lamplight, "
    "and the baker on the corner pulls the first loaves from an oven that has been warm "
    "since midnight. by six the tide has turned, and the boats slip out one by one, each "
    "leaving a short white line on the grey water. the children walk to school along the "
    "sea wall, counting gulls and arguing about whether the clouds mean rain. most days "
    "they are wrong. the weather here changes its mind three times before lunch, and the "
    "people who live by the water have learned to carry a coat in summer and to expect a "
    "bright hour in the middle of a winter storm. at the market, prices are written in "
    "chalk and corrected in pencil. a woman sells honey from her own hives and will tell "
    "you which hillside the bees visited that week; the clover honey is pale and sweet, "
    "the heather honey dark and sharp. a man who mends clocks keeps his door open so that "
    "the ticking spills into the street, and visitors stop to listen without knowing why. "
    "in the afternoon the boats return. the catch is sorted on the quay, the best fish "
    "packed in ice for the morning train, the rest sold to the restaurants along the "
    "front. gulls follow every crate. an old dog sleeps in the only patch of sun, "
    "undisturbed by the noise, as he has every afternoon for eleven years. when the "
    "light goes, the lamps come on along the harbor, and the reflections stretch and "
    "break on the moving water. someone plays an accordion outside the inn, badly but "
    "with great feeling. the baker is already asleep. the fishermen talk about the wind. "
    "the clock mender winds the largest clock in his shop, the one that has not been "
    "right since the year of the great flood, and then he winds it again, because he "
    "likes the sound. the town settles. the sea does not."
)


def char_probs(text):
    raise NotImplementedError


def huffman_code(probs):
    raise NotImplementedError


def encode(text, code):
    raise NotImplementedError


def decode(bits, code):
    raise NotImplementedError


def bits_per_char(text, code):
    raise NotImplementedError


def unigram_entropy(text):
    raise NotImplementedError


def bigram_conditional_entropy(text):
    raise NotImplementedError


REPORT = """
"""
