# Truth tables

A formula in $n$ propositions is a Python function of $n$ booleans, such as `lambda p, q: (not p) or q`.

- `implies(p, q)` returns the truth value of $p \Rightarrow q$.
- `truth_table(f, n)` returns a list of all $2^n$ rows, each a pair `(inputs, value)` where `inputs` is a tuple of $n$ booleans and `value` is `f(*inputs)`. Order the rows as in Section 1: `True` before `False`, with the first proposition changing slowest (for $n = 2$: TT, TF, FT, FF).
- `count_true(f, n)` returns how many rows are true.

`itertools.product([True, False], repeat=n)` produces exactly the rows in the right order; writing it yourself with recursion is also fine.

## Hints

1. `(not p) or q`.
2. `[(row, f(*row)) for row in itertools.product([True, False], repeat=n)]`.
3. `sum(...)` counts `True` as 1.
