# The source coding bound

Check Shannon's theorem from Section 2.

- `shannon_lengths(p)`: integer codeword lengths $\lceil -\log_2 p_i \rceil$.
- `kraft_sum(lengths)`: $\sum_i 2^{-\ell_i}$.
- `expected_length(p, lengths)`: $\sum_i p_i \ell_i$.
- `entropy_bits(p)`.

For any distribution, Shannon lengths satisfy Kraft's inequality and $H(p) \le \mathbb{E}[\ell] < H(p) + 1$. For a dyadic distribution (every $p_i$ a power of $\tfrac12$), the expected length equals the entropy.

## Hints

1. `np.ceil(-np.log2(p)).astype(int)`. Guard against tiny rounding: subtract `1e-12` inside the ceiling.
2. Kraft's sum uses powers of two.
3. The tests use probabilities strictly between 0 and 1.
