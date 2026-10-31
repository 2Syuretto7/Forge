# Seven shuffles

The puzzle, answered. The Gilbert-Shannon-Reeds model of a riffle shuffle cuts the deck at a binomial position and drops cards from the two halves with probability proportional to the sizes of what remains in each hand (Section 4). Bayer and Diaconis proved that after $k$ riffles of $n$ cards a permutation with $r$ **rising sequences** has probability $\binom{2^k + n - r}{n}/2^{kn}$, which depends only on $r$.

- `riffle(deck, rng)`: one GSR shuffle of a list; returns a new list.
- `rising_sequences(perm)`: for a deck listing the cards $0, \dots, n - 1$ in order of position, $1$ plus the number of cards $c$ for which card $c + 1$ lies above card $c$.
- `eulerian_counts(n)`: a dict mapping $r$ to the number of permutations of $n$ cards with $r$ rising sequences (the Eulerian numbers).
- `tv_after(k, n=52)`: the exact total variation distance from uniform after $k$ shuffles, $\frac12\sum_r A(n, r)\left\lvert\binom{2^k + n - r}{n}2^{-kn} - \frac1{n!}\right\rvert$, computed with `fractions.Fraction`.

The tests reproduce the famous table (0.924, 0.614, 0.334, 0.167 for 5 to 8 shuffles) and check the formula against your simulated shuffles of an 8-card deck.

## Hints

1. Eulerian numbers obey $A(m, r) = r\,A(m - 1, r) + (m - r + 1)\,A(m - 1, r - 1)$, starting from $A(1, 1) = 1$.
2. Python's integers are exact: `math.comb` and `Fraction` avoid every rounding problem in sums of numbers near $1/52!$.
3. In the shuffle, with $a$ cards left in the left hand and $b$ in the right, the next card comes from the left with probability $a/(a + b)$.
