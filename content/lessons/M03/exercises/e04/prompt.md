# Set operations from scratch

Python has a built-in `set` type with `|`, `&` and `-`. Build the operations yourself from loops, using lists without repeats and the `in` test, so that you know there is nothing inside them but logic.

Each function takes lists (with no repeated elements) and returns a list with no repeats:

- `union(A, B)`, `intersection(A, B)`, `difference(A, B)`;
- `is_subset(A, B)` returns a boolean;
- `product(A, B)` returns the list of all pairs `(a, b)`;
- `power_set(A)` returns the list of all subsets, each a list.

The tests compare your results with Python's sets (as sets, so order does not matter) and check an **invariant**: $|A \cup B| = |A| + |B| - |A \cap B|$ and the power set has $2^{|A|}$ elements, for random sets.

## Hints

1. `union`: start from a copy of `A`, then append each element of `B` not already present.
2. `power_set`: the subsets of `A` are the subsets of `A` without its first element, each with and without that first element.
3. `is_subset(A, B)` is "every element of A is in B".
