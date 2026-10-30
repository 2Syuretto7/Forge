# Families of functions

Build machines from descriptions.

- `polynomial(coeffs)`: for `coeffs = [c0, c1, ..., cn]`, the machine $x \mapsto c_0 + c_1 x + \dots + c_n x^n$, evaluated by **Horner's rule**: start from $c_n$ and repeatedly multiply by $x$ and add the next coefficient down.
- `rational(p, q)`: the machine $x \mapsto P(x)/Q(x)$ for coefficient lists `p` and `q`; raise `ValueError` where $Q(x) = 0$.
- `piecewise(pieces)`: for a list of `(lo, hi, f)` triples, the machine that applies the `f` of the first piece with `lo <= x < hi`, and raises `ValueError` if no piece contains `x`.

## Hints

1. `acc = 0` then `for c in reversed(coeffs): acc = acc * x + c`.
2. Build the two polynomials with your own `polynomial`.
3. Loop over the pieces and return as soon as one contains `x`.
