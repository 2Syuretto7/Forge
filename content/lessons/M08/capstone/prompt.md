# Capstone: exact against simulated

For each of ten puzzles, write an exact probability (a `Fraction`, by counting) and a one-trial simulator (a function of a `random.Random` that returns `True` or `False`). `PUZZLES` in the starter lists the names and descriptions:

| name | puzzle |
| --- | --- |
| `sum_seven` | two dice sum to 7 |
| `six_in_four` | at least one six in four rolls |
| `double_six_24` | at least one double six in 24 rolls of two dice |
| `birthday_23` | a shared birthday among 23 people |
| `two_aces` | two aces in two cards drawn from a deck |
| `full_house` | a full house in a 5-card hand |
| `three_heads` | at least three heads in a row somewhere in 10 fair coin flips |
| `derangement_10` | ten hats handed back at random, nobody gets their own |
| `committee` | a committee of 3 chosen from 10 people includes Ada |
| `same_suit_3` | three cards drawn from a deck are all of one suit |

Write `EXACT[name]` and `TRIALS[name]` for each, then:

- `report(n, seed=0)`: a list of dictionaries, one per puzzle, with keys `name`, `exact` (float), `estimate`, `se` (the standard error $\sqrt{p(1-p)/n}$) and `z`, simulating `n` trials of each puzzle with one `random.Random(seed)`.
- `hash_plan(n_docs, risk)`: a dictionary with `bits` (the shortest hash with expected colliding pairs at most `risk`) and `expected_pairs_64` (the expected colliding pairs with a 64-bit hash).

The tests check every exact value, require every $|z| \leq 3$ with 4,000 trials each, and check the hash plan for 10 million documents at a risk of $10^{-9}$.

Two of the exact values need more than one formula. For three heads in a row, count the sequences of 10 flips that avoid it: a sequence with no run of three ends in T, TH or THH after a shorter such sequence, which gives the recurrence $a_n = a_{n-1} + a_{n-2} + a_{n-3}$. For the derangements, $D_n = (n - 1)(D_{n-1} + D_{n-2})$ with $D_0 = 1$, $D_1 = 0$.
