# Degrees in a radian function

A colleague's code computed sines of angles that were stored in degrees, passing them straight to a function that expects radians. Given the inputs and the outputs it produced, decide which unit the code actually used.

- `sin_degrees(deg)`: the correct sine of an angle given in degrees.
- `units_used(inputs, outputs)`: return `"degrees"` if every output equals `sin_degrees` of its input (within `1e-9`), `"radians"` if every output equals `math.sin` of the raw input, and `"unknown"` otherwise.
- `suspicious(deg_inputs, outputs)`: `True` when the outputs claim to be sines of degree angles but at least one is far from `sin_degrees` (by more than 0.01). This is the check to run at the boundary of your code.

## Hints

1. `math.sin(math.radians(deg))`.
2. `all(abs(o - f(i)) < 1e-9 for i, o in zip(inputs, outputs))`.
3. Note that a few angles give similar answers in both units (0 does), so check them all.
