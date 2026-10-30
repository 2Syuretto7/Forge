# Evaluate an expression tree

An expression is a number, a variable name (a string), or a tuple `(op, left, right)` with `op` one of `"+"`, `"-"`, `"*"`, `"/"`, `"^"`. So $3x + 2$ is `("+", ("*", 3, "x"), 2)`.

Write `evaluate(expr, env)`, where `env` is a dictionary giving each variable's value, for example `{"x": 4.0}`:

- a number evaluates to itself;
- a string evaluates to `env[name]`;
- a tuple evaluates both operands, then applies the operation (`"^"` is `left ** right`).

A function that calls itself on smaller pieces is called **recursive**. Here the pieces are the operands, and the recursion stops at numbers and names.

Also write `variables(expr)`, returning the set of variable names that appear in the expression.

## Hints

1. `isinstance(expr, str)` tests for a name; `isinstance(expr, tuple)` for a tree; anything else is a number.
2. `op, a, b = expr` unpacks a tree; then `x, y = evaluate(a, env), evaluate(b, env)`.
3. For `variables`, return `{expr}` for a name, `set()` for a number, and the union `variables(a) | variables(b)` for a tree.
