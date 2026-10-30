# Break it: overflow, lost cents and the wrong unit

Numbers in a computer are not the real numbers of Section 1. This movement breaks three things on purpose: an integer that wraps around, money that leaks in floating point, and an estimate with a unit error. Predict each failure before you run it.

## Integers that wrap

NumPy's 32-bit integers hold whole numbers from $-2^{31} = -2{,}147{,}483{,}648$ to $2^{31} - 1 = 2{,}147{,}483{,}647$. One past the top does not raise an error.

::::predict{id=p5 kind=numeric answer=-2147483648 tol=0.5}
In 32-bit integer arithmetic, what is $2{,}147{,}483{,}647 + 1$?

:::reveal
$-2{,}147{,}483{,}648$. The 32 bits wrap around like an odometer, and the top bit of a signed integer means "negative", so one past the largest positive number is the most negative one. Counting the FLOPs of a large model in 32-bit integers overflows silently: $6ND$ for a 7-billion-parameter model on 2 trillion tokens is about $8 \times 10^{22}$, far past $2 \times 10^9$.
:::
::::

:::exercise{ref=e13}
:::

## Money in floating point

Floating-point numbers store a binary fraction, and most decimal fractions, $0.1$ included, have no exact binary form. Each addition rounds a little.

:::exercise{ref=e14}
:::

## The wrong unit

Below is a widget you already know, set to the training run. A colleague's estimate came out at 12,000 GPU-hours for the same run, and nobody noticed for a week. Read the factors: which conversion did they forget? The last exercise makes you find it from the numbers alone.

:::widget{name=MagnitudeLadder preset=train}
:::

:::exercise{ref=e15}
:::

## What to take away

- Integers in a computer have a range. Know it before you count anything big.
- Never store money, counts or identifiers in floating point.
- When an estimate is off by a round number such as 3,600, 1,000 or 1,024, suspect a unit before you suspect the physics.
