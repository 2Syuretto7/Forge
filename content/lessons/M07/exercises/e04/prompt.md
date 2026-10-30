# Complex numbers from scratch

Write a class `Complex` with attributes `re` and `im`:

- `Complex(re, im=0.0)`;
- `z + w`, `z - w` and `z * w` (Section 4's product), each returning a new `Complex`;
- `z.conj()`, the conjugate $a - bi$; `abs(z)` (the method `__abs__`), the modulus $\sqrt{a^2 + b^2}$;
- `z.arg()`, the angle, with `math.atan2`;
- `z.close(w, tol=1e-9)`, whether both parts agree within `tol`.

Also `from_polar(r, theta)`, a module-level function returning $r(\cos\theta + i\sin\theta)$.

The tests check an **invariant**: for random $z$, $w$, the modulus of the product is the product of the moduli and the angle of the product is the sum of the angles (up to whole turns), and $z \bar z = |z|^2$.

## Hints

1. `Complex(self.re * w.re - self.im * w.im, self.re * w.im + self.im * w.re)`.
2. `__abs__(self)` is what Python calls for `abs(z)`.
3. Compare angles by the cosine and sine of their difference, so whole turns do not matter.
