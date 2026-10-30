# Broken steps and broken bases

An argument by steps (induction, properly built in M05) proves $P(n)$ for every $n \geq n_0$ from two parts: the **base case** $P(n_0)$, and the **step** "$P(n)$ implies $P(n + 1)$" for every $n \geq n_0$. Both parts are needed. Here are two arguments, each missing one.

**Horses.** The step from $n$ horses to $n + 1$ uses two groups of $n$ horses that overlap in $n - 1$ horses. Write `overlap(n)`, the size of that overlap, `step_works(n)`, true when the overlap has at least one horse, and `first_broken_step()`, the smallest $n \geq 1$ whose step fails.

**Odd numbers.** "$n^2 + n$ is odd for every $n \geq 0$." Write `step_holds(n)`: if $n^2 + n$ were odd, would $(n + 1)^2 + (n + 1)$ be odd? Check it by testing whether the difference $(n+1)^2 + (n+1) - (n^2 + n) = 2n + 2$ is even (an odd number plus an even number is odd). And `base_holds()`: is $0^2 + 0$ odd? The step works for every $n$ and the base fails, so the claim is false everywhere, as `claim_holds(n)` (is $n^2 + n$ odd?) confirms.

## Hints

1. Two groups of $n$ from $n + 1$ horses share $n - 1$.
2. `(2 * n + 2) % 2 == 0`.
3. `(n * n + n) % 2 == 1`.
