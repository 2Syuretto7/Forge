# Puzzle: forty primes in a row

Consider the expression $n^2 + n + 41$. Evaluate it for $n = 0, 1, 2, \dots$:

| $n$ | 0 | 1 | 2 | 3 | 4 | 5 | 10 | 20 | 39 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $n^2 + n + 41$ | 41 | 43 | 47 | 53 | 61 | 71 | 151 | 461 | 1601 |

Every one of these is prime (divisible only by 1 and itself). In fact all forty values from $n = 0$ to $n = 39$ are prime. Leonhard Euler noticed this in 1772.

::::predict{id=p1 kind=choice answer=b}
What is $40^2 + 40 + 41$?

- Prime, like the forty before it.
- Composite: it equals $41 \times 41$.
- Composite: it is even.
- It cannot be decided without a computer.

:::reveal
$40^2 + 40 + 41 = 40 \cdot 40 + 40 + 41 = 40 \cdot 41 + 41 = 41 \cdot 41 = 1681$. Forty confirming cases, and the forty-first is a counterexample that you can find by hand once you look at the structure instead of the values. A reason (the factoring) beat a pile of evidence.
:::
::::

Forty cases looked like overwhelming evidence. They were not, and no number of cases ever is. Yet the expression is still remarkable: it produces primes unusually often.

::::predict{id=p2 kind=numeric answer=4149 tol=500}
For how many of the $n$ from 0 to 9,999 is $n^2 + n + 41$ prime? Give a count.

:::reveal
4,149, about 41 percent, far more than for a typical expression of the same size (whose values near $10^8$ are prime only about 5 percent of the time). The polynomial is special, which is why it fooled people. You will count this yourself in the build movement.
:::
::::

## Statements and their truth

The puzzle mixes three kinds of sentence:

- "$1681$ is prime" is a **statement**: definitely true or definitely false (here false).
- "$n^2 + n + 41$ is prime" is a **predicate**: its truth depends on $n$.
- "For every $n \geq 0$, $n^2 + n + 41$ is prime" is a **quantified** statement: a claim about all $n$ at once, and false, because of $n = 40$.

The widget compares two statements built from smaller ones. Pick "An implication and its converse", the two statements "if it rains, the street is wet" and "if the street is wet, it rained". Do they say the same thing? The table checks every combination of true and false.

:::widget{name=TruthTable pair=converse}
:::

## Questions to carry into the derivation

1. What exactly does "if p then q" claim, and how is it related to "if not q then not p"?
2. How do you negate "for every" and "there exists"?
3. What are sets and functions, made precise?
4. What are the ways to prove a statement about infinitely many cases?
