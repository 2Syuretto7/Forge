# Puzzle: 92 percent on a thousand examples

A model gets 920 of 1,000 test examples right.

::::predict{id=p1 kind=numeric answer=4.3 tol=0.6}
How far, in percentage points, could the true accuracy be from 92 percent, guaranteed with probability 95 percent for any distribution of errors, assuming only that the examples are independent?

:::reveal
About $4.3$ points: Hoeffding's inequality gives $\sqrt{\ln(2/0.05)/(2 \times 1000)} \approx 0.043$. It uses nothing but the range of each outcome, 0 or 1, and holds for every distribution with that range.
:::
::::

::::predict{id=p2 kind=choice answer=c}
The central limit theorem's 95 percent interval for the same result is narrower. By how much?

- About the same.
- About $\pm 3$ points.
- About $\pm 1.7$ points.
- About $\pm 0.4$ points.

:::reveal
About $\pm 1.7$: $1.96\sqrt{0.92 \times 0.08/1000} \approx 0.017$. It uses the small variance of a coin with $p$ near 1 and is usually right, but it is an approximation. Hoeffding's interval is two and a half times wider and is a guarantee.
:::
::::

The exact chance that the average of $n$ flips misses $p$ by at least $\varepsilon$, with the two bounds and the normal approximation. The bounds always lie above the truth; Hoeffding's falls exponentially, Chebyshev's only like $1/n$.

:::widget{name=ConcentrationMeter p=0.92 eps=0.03 maxn=2000}
:::

## Questions to carry into the derivation

1. What is the sharpest guarantee for an average of bounded variables?
2. What does it cost to make the guarantee hold for many models at once?
3. How can a class with infinitely many models still generalize?
4. Why does reusing a test set break every one of these guarantees?
