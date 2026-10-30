# Scale: a thousand integrals to eight digits

Integrate a thousand functions $e^{-ax}\cos(bx)$ on $[0, 1]$ to $10^{-8}$, with the trapezoid rule, Simpson's rule and adaptive Simpson, and count the evaluations each needs.

::::predict{id=p4 kind=choice answer=c}
The trapezoid rule needs about 16,000 strips for $\int_0^\pi \sin x\,dx$ to $10^{-8}$. About how many does Simpson's rule need?

- About 16,000, the same.
- About 2,000.
- About 120.
- About 12.

:::reveal
About 120. Simpson's error shrinks like $h^4$ instead of $h^2$: from $\frac{\pi^5}{180n^4} \leq 10^{-8}$, $n \approx 114$, rounded up to an even 116. Higher order pays enormously for smooth functions; the same order collapses for functions with corners or singularities, which is why adaptive methods check their own error instead of trusting a formula.
:::
::::

:::exercise{ref=e10}
:::

:::exercise{ref=e11}
:::

:::exercise{ref=e12}
:::

The widget's strips for $\sin(25x)$: with fewer than a few strips per wiggle the sum is meaningless, with enough it converges at the usual rate.

:::widget{name=RiemannSum f=wiggle rule=simpson n=8}
:::
