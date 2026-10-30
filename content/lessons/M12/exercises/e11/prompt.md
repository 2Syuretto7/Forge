# What each method costs

Count operations for a tall $m \times n$ problem (one multiply-add counts 2).

- `flops_normal(m, n)`: forming $A^\top A$ using its symmetry ($mn^2$, half the products of a full $n \times n$ result) plus forming $A^\top b$ ($2mn$) plus solving by Cholesky ($n^3/3$).
- `flops_qr(m, n)`: Householder QR, $2mn^2 - \frac{2}{3}n^3$, plus applying $Q^\top$ to $b$ ($4mn$) and back substitution ($n^2$).
- `ratio(m, n)`: `flops_qr / flops_normal`.

For $m \gg n$ QR costs about twice as much: the price of its extra digits. Then time both on a $20000 \times 50$ problem in the console.

## Hints

1. Use floats; the formulas have fractions.
2. As $m/n$ grows, `ratio` tends to 2.
3. For square problems ($m = n$) the ratio is about $(4/3)/(4/3) = 1$ plus lower-order terms.
