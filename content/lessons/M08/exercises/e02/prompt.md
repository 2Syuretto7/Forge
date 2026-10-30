# Factorials and permutations

- `factorial(n)`: $n!$ with a loop, exactly (Python integers never overflow); $0! = 1$.
- `arrangements(n, k)`: ordered selections of $k$ from $n$, $n!/(n-k)!$, computed as a product of $k$ factors (do not divide huge factorials).
- `all_permutations(items)`: the list of every ordering of the list `items`, each a list, by recursion: each item in turn comes first, followed by every ordering of the rest.

The tests check an **invariant**: for lists of length up to 7, the number of orderings you list is $n!$, they are all different, and each uses every item once.

## Hints

1. Start from 1 and multiply by $2, 3, \dots, n$.
2. `n * (n - 1) * ... * (n - k + 1)`.
3. The base case: the empty list has exactly one ordering, `[[]]`.
