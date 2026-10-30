# Find the planted errors

The starter contains `CHAIN`, a derivation written as a list of expressions, each claimed equal to the one before, and the variables it uses. Two of its steps are wrong. It also provides `evaluate`.

Write `bad_steps(chain, names, trials=50, seed=0)`: the list of indices `i` such that `chain[i]` is **not** the same function as `chain[i - 1]`, found by testing at random points as in the build movement (skip points where an expression divides by zero; values uniform in $[-10, 10]$; tolerance `1e-9 * max(1, abs(value))`).

Before you run anything, read the chain and predict which two steps are wrong.

## Hints

1. Loop `for i in range(1, len(chain))` and compare neighbours.
2. A step is bad if any random point gives different values.
3. The answer is a list of two indices. Notice that the chain still ends at the right answer: two errors can cancel, which is why checking the final result alone is not enough.
