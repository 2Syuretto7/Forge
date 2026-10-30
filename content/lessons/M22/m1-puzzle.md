# Puzzle: the sum of 512 small numbers

A neuron's input is the sum of 512 terms. Suppose each term is $+0.01$ or $-0.01$, decided by a fair coin, independently.

::::predict{id=p1 kind=numeric answer=0.23 tol=0.03}
How large is the sum typically? Give its standard deviation.

:::reveal
About $0.23$. Each term has mean 0 and variance $0.01^2 = 10^{-4}$. Independent variances add, so the sum has variance $512 \times 10^{-4} = 0.0512$ and standard deviation $\sqrt{0.0512} \approx 0.226$. Not $5.12$, which needs every coin to agree, and not 0: the terms cancel, but not completely, and the leftover imbalance grows like $\sqrt{512} \approx 22.6$ terms' worth.
:::
::::

::::predict{id=p2 kind=choice answer=b}
The layer is made four times wider: 2,048 terms of the same kind. What happens to the typical size of the sum?

- It stays the same.
- It doubles.
- It becomes four times larger.
- It becomes sixteen times larger.

:::reveal
It doubles: the variance is four times larger and the standard deviation is its square root. This is why initializations scale weights by $1/\sqrt{n}$ for $n$ inputs: that keeps the sum's size independent of the width.
:::
::::

## Questions to carry into the derivation

1. What exactly is a random variable, and how is its distribution described?
2. Why can you add expectations without knowing anything about dependence?
3. When do variances add, and what goes wrong when they do not?
4. How do you produce samples of any distribution from uniform random numbers?
