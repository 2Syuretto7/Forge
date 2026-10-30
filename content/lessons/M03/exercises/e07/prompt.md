# Primes and Euler's polynomial

- `is_prime(n)`: `True` for primes, by trial division by every $d$ with $2 \leq d$ and $d^2 \leq n$. Numbers below 2 are not prime.
- `first_composite(poly, start=0)`: the first $n \geq$ `start` at which `poly(n)` is not prime.
- `prime_count(poly, N)`: how many of `poly(0)`, ..., `poly(N - 1)` are prime.
- `factor_pair(m)`: for a composite `m`, the pair `(d, m // d)` with `d` its smallest divisor above 1.

Then check the puzzle: $n^2 + n + 41$ first fails at $n = 40$, and among $n < 10{,}000$ it is prime 4,149 times.

## Hints

1. `d * d <= n` avoids computing square roots.
2. `while is_prime(poly(n)): n += 1`.
3. `factor_pair` uses the same trial division.
