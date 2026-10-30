# The contrapositive, checked

To prove "if $n^2$ is even then $n$ is even" the derivation proved "if $n$ is odd then $n^2$ is odd". Check, on many cases, that a statement and its contrapositive fail at exactly the same cases, and that the converse is a different statement.

- `failures(p, q, cases)`: the cases where $p \Rightarrow q$ fails ($p$ true, $q$ false).
- `contrapositive_failures(p, q, cases)`: the cases where (not $q$) $\Rightarrow$ (not $p$) fails.
- `converse_failures(p, q, cases)`: the cases where $q \Rightarrow p$ fails.

Here `p` and `q` are predicates of one case. The tests check an **invariant**: for many random predicates on random cases, the failure lists of a statement and its contrapositive are identical.

## Hints

1. `[x for x in cases if p(x) and not q(x)]`.
2. For the contrapositive, the hypothesis is `not q(x)` and the conclusion `not p(x)`.
3. Swap `p` and `q` for the converse.
