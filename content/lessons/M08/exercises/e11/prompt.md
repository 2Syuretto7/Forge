# Hash collisions, predicted and simulated

- `expected_colliding_pairs(n, bits)`: $\binom{n}{2} / 2^{\text{bits}}$.
- `p_any_collision(n, bits)`: about $1 - e^{-\binom{n}{2}/2^{\text{bits}}}$.
- `simulated_colliding_pairs(n, bits, seed=0)`: draw `n` hash values uniformly from $[0, 2^{\text{bits}})$ with NumPy (`rng.integers(0, 2 ** bits, size=n, dtype=np.int64)`), and count colliding pairs exactly: a value appearing $c$ times contributes $\binom{c}{2}$ pairs.

The tests simulate 100,000 items with 24-bit and 32-bit hashes and compare with the prediction.

## Hints

1. `math.comb(n, 2) / 2 ** bits`.
2. `np.unique(values, return_counts=True)`.
3. `int(np.sum(counts * (counts - 1) // 2))`.
