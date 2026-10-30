# Simplify an expression

Write `simplify(expr)` applying these rules, bottom-up (simplify the operands first, then the tree itself):

- **constant folding:** an operation on two numbers becomes its value, so `("+", 2, 3)` becomes `5`;
- `x + 0` and `0 + x` become `x`; `x - 0` becomes `x`;
- `x * 1` and `1 * x` become `x`; `x * 0` and `0 * x` become `0`;
- `x / 1` becomes `x`; `x ^ 1` becomes `x`; `x ^ 0` becomes `1`;
- `x - x` becomes `0` when both sides are the same tree (compare with `==`).

Every rule is one of the field rules of Section 2 or follows from them. Leave division by the number 0 alone (do not fold it); that is not your simplifier's problem to solve.

The tests check an **invariant**: for random expressions and random values of the variables, the simplified expression has the same value as the original.

## Hints

1. `if not isinstance(expr, tuple): return expr`; otherwise `op, a, b = expr` and `a, b = simplify(a), simplify(b)`.
2. Test the "is a number" case with `isinstance(a, (int, float))`.
3. Return `(op, a, b)` when no rule applies.
