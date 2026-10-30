# Ordered on top, unordered below

Two cards are drawn without replacement from a 52-card deck with 4 aces.

- `p_two_aces()`: the correct probability, counting unordered hands on both sides: $\binom{4}{2} / \binom{52}{2}$, as a `Fraction`.
- `p_two_aces_ordered()`: also correct, counting ordered draws on both sides: $(4 \cdot 3)/(52 \cdot 51)$.
- `p_two_aces_mixed()`: the mistake: ordered favourable draws over unordered hands.
- `mismatch_factor(k)`: how much the mixed count overstates a probability when $k$ cards are drawn ($k!$, the number of orders of each hand).
- `simulate(n, seed=0)`: the simulated fraction of `n` draws (with `random.Random(seed).sample(deck, 2)`) that give two aces.

## Hints

1. `Fraction(math.comb(4, 2), math.comb(52, 2))`.
2. The two correct versions are equal, which is the point.
3. The mixed version is exactly `math.factorial(2)` times too big.
