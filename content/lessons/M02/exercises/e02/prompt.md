# Print an expression

Write `to_string(expr)` that turns a tree back into the usual notation:

- a number prints as `str(number)` and a variable as its name;
- a tree prints as `(left op right)` with single spaces around the operator, so `("+", ("*", 3, "x"), 2)` prints as `((3 * x) + 2)`.

Every operation gets its own parentheses. That is uglier than school notation but never ambiguous, and ambiguity is where algebra mistakes hide: $a - b - c$ means $(a - b) - c$, but a reader in a hurry can see $a - (b - c)$.

Then write `count_operations(expr)`, the number of operations (tuples) in the tree, and `depth(expr)`, the length of the longest chain of nested operations (a number or name has depth 0).

## Hints

1. `f"({to_string(a)} {op} {to_string(b)})"`.
2. `count_operations` of a tree is 1 plus the counts of its operands.
3. `depth` of a tree is 1 plus the larger depth of its operands.
