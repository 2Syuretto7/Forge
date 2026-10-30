# Poker hands

A 5-card hand from 52 cards (13 ranks, 4 suits) is one of $\binom{52}{5} = 2{,}598{,}960$ equally likely hands. Count by stages:

- `full_houses()`: three cards of one rank and two of another. Choose the rank of the three, which three suits, the rank of the pair (a different rank), which two suits.
- `flushes()`: all five cards of one suit, **excluding** straight flushes (five consecutive ranks, of which there are 10 per suit, counting ace-low and ace-high).
- `two_pairs()`: two cards of each of two ranks and one card of a fifth rank. Choose the two pair ranks together (an unordered pair), their suits, then the fifth card.
- `probability(count)`: `count` divided by the number of hands, as a float.

The tests also count by brute force over a smaller deck, to check your method rather than your memory.

## Hints

1. `13 * C(4, 3) * 12 * C(4, 2)`.
2. `4 * (C(13, 5) - 10)`.
3. `C(13, 2) * C(4, 2) ** 2 * 44`: the last card avoids both pair ranks.
