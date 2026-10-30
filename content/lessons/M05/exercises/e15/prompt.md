# Induction with a broken part

Each claim below says $\sum_{k=1}^n f(k) = F(n)$ for every $n \geq 1$. Check the two parts of induction **numerically** this time, for $n$ up to 50, and say which part fails.

- `base_ok(f, F)`: $F(1) = f(1)$.
- `step_ok(f, F, max_n=50)`: $F(n + 1) - F(n) = f(n + 1)$ for every $n$ from 1 to `max_n`.
- `claim_ok(f, F, max_n=50)`: the claim itself holds for every $n$ from 1 to `max_n` (compute the sum directly).
- `diagnose(f, F)`: `"proved"` if both parts hold, `"no base"` if only the step holds, `"no step"` if only the base holds, `"neither"` otherwise.

Use exact `Fraction` arithmetic so equalities are exact. The starter provides `CLAIMS`, four claims with their names; the tests check your diagnosis of each.

## Hints

1. `Fraction(F(1)) == Fraction(f(1))`.
2. A claim with a working step but no base is false everywhere it was claimed, or shifted by a constant.
3. `claim_ok` agrees with `diagnose` being `"proved"` on these examples, but that is not a coincidence: it is the theorem of induction.
