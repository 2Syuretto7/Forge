# Powers and roots from scratch

- `power_int(a, n)`: $a^n$ for any integer $n$ (negative too), by repeated multiplication; `power_int(a, 0)` is 1.
- `nth_root(a, n)`: the positive $n$-th root of $a > 0$, by bisection on $x \mapsto x^n$ (as in M04). Bracket it with $[0, \max(1, a)]$ and halve 100 times.
- `power_rational(a, p, q)`: $a^{p/q} = (a^{1/q})^p$ for $a > 0$ and integers $p$, $q > 0$.

The tests check an **invariant**: the power rule $a^m a^n = a^{m+n}$ holds for your `power_int` on many random inputs, and $(a^{1/q})^q = a$.

## Hints

1. For negative $n$, compute `power_int(a, -n)` and take its reciprocal.
2. For $a < 1$ the root is bigger than $a$, which is why the bracket goes up to $\max(1, a)$.
3. `power_int(nth_root(a, q), p)`.
