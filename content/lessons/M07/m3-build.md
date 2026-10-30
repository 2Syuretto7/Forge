# Build: angles, rotations and complex numbers

You will build angle conversions, rotations two ways (by trigonometry and by complex multiplication), a complex number class from scratch, Euler's formula from the series, and a toy version of the rotary position encoding used in transformers.

Python has a built-in complex type (`3 + 4j`). Build your own first; afterwards you may use the built-in one, and in Movement 4 NumPy's.

## Angles and the circle

:::exercise{ref=e01}
:::

:::exercise{ref=e02}
:::

## Rotation two ways

:::exercise{ref=e03}
:::

:::exercise{ref=e04}
:::

:::exercise{ref=e05}
:::

## Formulas, checked

:::exercise{ref=e06}
:::

:::exercise{ref=e07}
:::

:::exercise{ref=e08}
:::

## A rotary position encoding

A transformer compares tokens by dot products of query and key vectors. The rotary encoding turns each pair of coordinates of a vector by an angle proportional to the token's position. The dot product of a turned query and a turned key then depends only on the difference of their positions: exactly the relative information attention needs.

:::exercise{ref=e09}
:::
