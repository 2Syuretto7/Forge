# Domains that fail loudly

A function is its rule **and** its domain. Build machines that refuse inputs outside their domain with a clear `ValueError`.

- `with_domain(f, ok, name)` returns a machine that computes `f(x)` when `ok(x)` is true and otherwise raises `ValueError(f"{name}: {x} is outside the domain")`.
- `safe_sqrt`, `safe_log` and `safe_reciprocal`: machines built with `with_domain` for $\sqrt{x}$ ($x \geq 0$), $\ln x$ ($x > 0$, using `math.log`) and $1/x$ ($x \neq 0$). Define them at module level.
- `in_composite_domain(f_ok, g, g_ok, x)`: whether `x` is in the domain of $f \circ g$, that is `g_ok(x)` and `f_ok(g(x))`.

## Hints

1. Inside the returned machine: `if not ok(x): raise ValueError(...)`.
2. `safe_sqrt = with_domain(math.sqrt, lambda x: x >= 0, "sqrt")`.
3. Check `g_ok(x)` first, so that `g(x)` is only computed where it is defined.
