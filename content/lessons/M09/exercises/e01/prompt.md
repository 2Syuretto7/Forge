# A vector class without NumPy

Write `Vec`, a vector stored as a Python list:

- `Vec(coords)` stores `self.c` as a list of floats;
- `v + w`, `v - w`, and `v * k` and `k * v` for a number `k`;
- `v.dot(w)`, `v.norm()` and `len(v)` (the method `__len__`);
- `v.unit()`: the unit vector, raising `ValueError` for the zero vector.

Adding vectors of different lengths raises `ValueError`.

The tests check an **invariant**: for random vectors, the dot product is symmetric and linear, $(a u + b v) \cdot w = a\, u \cdot w + b\, v \cdot w$, and $\|k v\| = |k|\,\|v\|$.

## Hints

1. `Vec([a + b for a, b in zip(self.c, w.c)])` after checking the lengths.
2. `__rmul__` handles `k * v`.
3. `math.sqrt(self.dot(self))`.
