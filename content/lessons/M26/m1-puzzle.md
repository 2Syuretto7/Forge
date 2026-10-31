# Puzzle: adding one

In float32, $16{,}777{,}216 + 1 = 16{,}777{,}216$.

::::predict{id=p1 kind=numeric answer=16777216 tol=1}
Start a float32 total at 0 and add 1.0 to it a hundred million times. What is the final total?

:::reveal
$16{,}777{,}216 = 2^{24}$. Float32 keeps 24 significant bits. Past $2^{24}$ the gap between consecutive floats is 2, so $2^{24} + 1$ lies exactly halfway and rounds to the even neighbour, $2^{24}$ itself, and the total never moves again. Every further addition is silently lost.
:::
::::

::::predict{id=p2 kind=choice answer=b}
Which ordinary computation is most likely to go silently wrong in the same way?

- The mean of ten numbers near 1.
- The variance of Unix timestamps near $1.7 \times 10^9$ seconds, computed in float64 as the mean of the squares minus the square of the mean.
- The maximum of a list.
- Sorting a list of floats.

:::reveal
The variance. Both terms are near $2.9 \times 10^{18}$, where even float64's gap between neighbouring numbers is 512, while their difference, the variance, is perhaps 1. The result is rounding noise, hundreds or thousands, sometimes negative, and nothing warns you. Section 3 explains why, and Section 6 and the break movement fix it.
:::
::::

Type a number and see how each format stores it: sign, exponent, fraction, and the error of the stored value. Try $16777217$, $0.1$, and $65520$ in fp16.

:::widget{name=FloatFormats value=16777217}
:::

## Questions to carry into the derivation

1. How exactly is a floating-point number stored, and how far apart are neighbouring ones?
2. How large can the error of one rounding be?
3. Which formulas turn small rounding errors into large ones?
4. How do you compute softmax, log-sigmoid and sums so that they never fail?
