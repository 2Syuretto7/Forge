# Break it: a version counter for in-place updates

Two helpers detect the bug from this movement:

- `mul_(t, s)` scales `t.data` in place by the number `s` and increments `t._version` (treat a missing attribute as version 0).
- `checked_mul(a, b)` computes `a * b` like the engine's multiply, but records the versions of `a` and `b` at forward time; its backward rule raises `RuntimeError` if either has changed since, instead of silently using modified values.

The tests run the bug both ways: an unprotected multiply that returns a wrong gradient, and your checked one that raises.

## Hints

1. Use `getattr(t, "_version", 0)` so tensors created before you added the counter still work.
2. Capture the versions in local variables in `checked_mul`, and compare inside the closure.
3. The gradient rule itself is unchanged: `unbroadcast(out.grad * b.data, a.shape)` to `a` and the mirror image to `b`.
