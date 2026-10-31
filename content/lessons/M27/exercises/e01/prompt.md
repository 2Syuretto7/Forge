# Surprisal and entropy

Implement Section 1 for distributions given as 1-D arrays of probabilities.

- `surprisal(p, base)`: elementwise $-\log_{\text{base}} p$ (infinite where $p = 0$).
- `entropy(p, base)`: $-\sum p \log_{\text{base}} p$ with $0 \log 0 = 0$. `base` is `2` for bits or `np.e` for nats.
- `to_bits(nats)`: convert a quantity in nats to bits.

## Hints

1. $\log_b x = \ln x / \ln b$.
2. Mask zero probabilities before taking logs: `p[p > 0]`.
3. Use `np.errstate(divide="ignore")` when computing surprisals of zero probabilities.
