# Composition

- `compose(f, g)` returns the machine $x \mapsto f(g(x))$: `g` first.
- `compose_all(fs)` composes a list of machines so that the **last** in the list acts first: `compose_all([f, g, h])(x)` is `f(g(h(x)))`. The empty list gives the identity machine $x \mapsto x$.
- `commute_points(f, g, xs)` returns the list of the `x` in `xs` where $f(g(x))$ and $g(f(x))$ agree to within `1e-12`.

The tests check an **invariant**: composition is associative. For random machines `f`, `g`, `h` and random inputs, `compose(f, compose(g, h))` and `compose(compose(f, g), h)` give the same output.

## Hints

1. `return lambda x: f(g(x))`.
2. Start with the identity and compose from the right: loop over `reversed(fs)`, applying each in turn.
3. `abs(f(g(x)) - g(f(x))) <= 1e-12`.
