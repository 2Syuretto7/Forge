# Counting loop iterations

Count how many times the innermost body runs, by running the loops and counting, and compare with the closed forms of the derivation.

- `count_pairs(n)`: `for i in range(n): for j in range(i):` count.
- `count_triples(n)`: `for i in range(n): for j in range(i): for k in range(j):` count.
- `count_halvings(n)`: how many times `while m > 0: m //= 2` runs, starting from `m = n`.
- `formulas(n)`: the triple `(pairs, triples, halvings)` from closed forms: $\binom{n}{2}$, $\binom{n}{3}$ and the number of binary digits of $n$ (`n.bit_length()`).

## Hints

1. A counter `c = 0` and `c += 1` in the innermost body.
2. $\binom{n}{3} = n(n - 1)(n - 2)/6$.
3. Halving $n$ until it reaches 0 takes as many steps as $n$ has binary digits.
