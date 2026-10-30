# Break it: no pivoting, a bad tolerance, a nearly repeated sensor

## Remove the pivoting

::::predict{id=p4 kind=choice answer=c}
Solving $10^{-20} x_1 + x_2 = 1$, $x_1 + x_2 = 2$ by elimination without row swaps in double precision, how many correct digits does $x_1$ have?

- All 16: the arithmetic is exact for such simple numbers.
- About 8: half are lost.
- None: $x_1$ comes out as 0 instead of nearly 1.
- The program crashes with a division by zero.

:::reveal
None. Section 3 traced it: $1 - 10^{20}$ rounds to $-10^{20}$, the information in the second equation is wiped out, and back substitution returns $x_1 = 0$. Nothing crashes and nothing warns. With partial pivoting the same arithmetic gives both unknowns to full precision.
:::
::::

:::exercise{ref=e13}
:::

## Pick the rank tolerance badly

:::exercise{ref=e14}
:::

## A sensor that nearly repeats another

::::predict{id=p5 kind=choice answer=a}
The second sensor reads $2.001$ times the first sensor's weights instead of exactly twice. The system now has a unique solution. If one reading changes by 0.001, how far can the solution move?

- By about 1 or more: the nearly dependent rows amplify small changes a thousandfold.
- By about 0.001, like the reading.
- Not at all: the solution is unique.
- By exactly 0.002, twice the change.

:::reveal
By about 1 or more. Two nearly parallel equations cross at a point that slides far when either moves, the picture from M02 in more dimensions. The amplification factor is the **condition number** of the matrix; M14 computes it from singular values and M26 makes it the measure of how many digits a computation can lose.
:::
::::

:::exercise{ref=e15}
:::

:::widget{name=MatrixTransform a=1 b=2 c=0.5 d=1.001}
:::

The determinant here is $0.001$: the ellipse is a long, thin needle. Points far apart along the needle's narrow direction land close together, and undoing the map pulls them apart again, amplifying any error.

## What to take away

- Always pivot. The algebra is the same; the floating-point result is not.
- A rank is only as meaningful as its tolerance, and the tolerance should reflect how accurately the data were measured.
- A unique solution can still be useless when the rows are nearly dependent.
