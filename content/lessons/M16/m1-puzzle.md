# Puzzle: sin(0.1) with additions and multiplications

A calculator's chip can add and multiply. Yet it reports $\sin(0.1) = 0.0998334166468\ldots$ How?

::::predict{id=p1 kind=numeric answer=3 tol=0.01}
The chip uses $\sin x \approx x - \frac{x^3}{6} + \frac{x^5}{120} - \dots$. How many nonzero terms make the error at $x = 0.1$ smaller than $10^{-10}$?

:::reveal
Three. After $x - x^3/6$ the next term is $x^5/120 \approx 8.3 \times 10^{-8}$, too big; after three terms it is $x^7/5040 \approx 2 \times 10^{-11}$. For an alternating series with shrinking terms, the error is smaller than the first term left out. Real libraries first reduce the argument into a small interval (using $\sin(x + 2\pi) = \sin x$ and other identities), where a handful of terms reaches full double precision.
:::
::::

::::predict{id=p2 kind=numeric answer=6 tol=1}
Newton's method for $\sqrt 2$ replaces $x$ by $\frac12 (x + 2/x)$. From $x = 1.5$, which has 1 correct digit, the next value $17/12 = 1.41667$ has 3. About how many correct digits does the next value have?

:::reveal
About 6: $577/408 = 1.4142157$, against $\sqrt 2 = 1.4142136$. The error went from $2.5 \times 10^{-3}$ to $2.1 \times 10^{-6}$, roughly its square. The next step has 12 digits, and the one after that the full 16. Section 5 proves the doubling.
:::
::::

Raise the degree and watch the polynomial hug the sine over a wider range; read the error at the evaluation point. Then try $\log(1 + x)$ beyond $x = 1$, where adding terms makes things worse.

:::widget{name=TaylorBuilder f=sin a=0 n=3 x=0.1}
:::

## Questions to carry into the derivation

1. Why does a polynomial built from derivatives at one point approximate the function elsewhere, and how well?
2. How can you tell a minimum from a maximum without plotting?
3. Why does Newton's method double the correct digits?
4. How large can a gradient-descent step be before it overshoots for ever?
