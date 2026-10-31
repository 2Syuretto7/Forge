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
    c = Counter(text)
    n = len(text)
    return {ch: k / n for ch, k in c.items()}


def huffman_code(probs):
    if len(probs) == 1:
        return {next(iter(probs)): "0"}
    heap = []
    counter = 0
    for ch, p in sorted(probs.items()):
        heap.append((p, counter, {ch: ""}))
        counter += 1
    heapq.heapify(heap)
    while len(heap) > 1:
        p1, _, c1 = heapq.heappop(heap)
        p2, _, c2 = heapq.heappop(heap)
        merged = {ch: "0" + w for ch, w in c1.items()}
        merged.update({ch: "1" + w for ch, w in c2.items()})
        heapq.heappush(heap, (p1 + p2, counter, merged))
        counter += 1
    return heap[0][2]


def encode(text, code):
    return "".join(code[ch] for ch in text)


def decode(bits, code):
    inverse = {w: ch for ch, w in code.items()}
    out = []
    cur = ""
    for b in bits:
        cur += b
        if cur in inverse:
            out.append(inverse[cur])
            cur = ""
    return "".join(out)


def bits_per_char(text, code):
    return len(encode(text, code)) / len(text)


def _entropy_bits(counts):
    n = sum(counts.values())
    return -sum(k / n * math.log2(k / n) for k in counts.values())


def unigram_entropy(text):
    return _entropy_bits(Counter(text))


def bigram_conditional_entropy(text):
    pairs = Counter(zip(text[:-1], text[1:]))
    firsts = Counter(text[:-1])
    return _entropy_bits(pairs) - _entropy_bits(firsts)


# your answer
REPORT = """
On this corpus the unigram entropy is about 4.1 bits per character, and the Huffman code
achieves about 4.15 bits per character, compared with 8 bits for plain one-byte storage.
Huffman must use a whole number of bits per codeword, so it cannot reach the entropy exactly
unless every probability is a power of one half, but it is optimal among prefix codes and
always lands within one bit of the entropy; here it is within a few hundredths of a bit.
The bigram conditional entropy is clearly lower, about 3.0 bits, because knowing the previous
character makes the next one more predictable: after q comes u, after a space a consonant
is likely. That estimate is optimistic for such a short text, since many pairs are seen
only once. A language model that conditions on a long context predicts each character far
better still, and arithmetic coding driven by its probabilities would approach its
cross-entropy, around one to two bits per character for English, far below the unigram rate.
"""
