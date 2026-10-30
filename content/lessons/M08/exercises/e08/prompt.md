# Inclusion-exclusion

The size of a union of several finite sets, without listing the union:

$$
|A_1 \cup \dots \cup A_n| = \sum_{\varnothing \neq S \subseteq \{1..n\}} (-1)^{|S| + 1} \left| \bigcap_{i \in S} A_i \right| .
$$

Add the sizes of single sets, subtract the pairwise intersections, add back the triple ones, and so on.

- `union_size(sets)`: by that formula, looping over every non-empty group of the sets (`itertools.combinations`), using only intersections.
- `count_divisible(n, divisors)`: how many of $1, \dots, n$ are divisible by at least one of the divisors, by the same formula, with $|\{k \leq n : d_1, \dots, d_j \text{ all divide } k\}| = \lfloor n / \operatorname{lcm}(d_1, \dots, d_j) \rfloor$.

The tests check an **invariant**: for random families of sets, the formula agrees with Python's `set.union`.

## Hints

1. `for r in range(1, len(sets) + 1): for group in itertools.combinations(sets, r):`.
2. `set.intersection(*group)`.
3. `math.lcm(*group)` (Python 3.9 and later).
