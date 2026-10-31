# A million actions at any temperature

Compute the Gibbs distribution over $10^6$ actions with rewards drawn from the starter's `make_rewards(seed=0)`, across temperatures from $10^{-3}$ to $10^3$, without a single overflow or `nan`.

- `entropy(p)`: in nats, with $0\log 0 = 0$.
- `sweep(r, taus)`: for each temperature, the entropy and the expected reward of the Gibbs distribution (e08), as two arrays.
- `effective_actions(p)`: $e^{H(p)}$, the number of equally likely actions with the same entropy.

The tests check the limits (at low temperature the mass sits on the best few actions, at high temperature it spreads over nearly all $10^6$), that entropy rises and expected reward falls with temperature, and that every value is finite.

## Hints

1. Subtract the maximum reward before dividing by $\tau$, as in M26.
2. $H = \log Z - \frac1\tau(\mathbb{E}r - \max r)$ with $Z = \sum e^{(r - \max r)/\tau}$ avoids logarithms of tiny probabilities.
3. Expected reward is a weighted mean: `p @ r`.
