# Break it: false theorems with plausible proofs

Every rule of proof has a condition. Here are three "proofs" of false statements. Each has exactly one faulty step. Predict the faulty step before you run anything.

## One equals two

Let $a = b$. Then $a^2 = ab$, so $a^2 - b^2 = ab - b^2$, so $(a + b)(a - b) = b(a - b)$, so $a + b = b$, so $2b = b$, so $2 = 1$.

:::exercise{ref=e13}
:::

## All horses are the same colour

"Proof": one horse is the same colour as itself. Suppose any $n$ horses are the same colour, and take $n + 1$ horses. The first $n$ are the same colour, and so are the last $n$. The two groups overlap, so all $n + 1$ are the same colour.

::::predict{id=p5 kind=choice answer=b}
Where does the argument fail?

- The base case: one horse is not always the same colour as itself.
- The step from 1 horse to 2: the "first one" and the "last one" do not overlap.
- The step from 99 horses to 100.
- Nowhere; the conclusion is just surprising.

:::reveal
With $n + 1 = 2$ horses, the first group is horse 1 and the last group is horse 2. They share no horse, so nothing links their colours. Every step from $n \geq 2$ works, because two groups of $n$ out of $n + 1$ overlap in $n - 1 \geq 1$ horses. One broken link in a chain of dominoes stops everything after it.
:::
::::

:::exercise{ref=e14}
:::

## Swapping quantifiers

The last false proof hides in word order. "For every $x$ there is a $y$" quietly becomes "there is a $y$ for every $x$". Find a small example where the first is true and the second false.

:::widget{name=TruthTable pair=wrongDemorgan}
:::

The table above shows the most common slip of all when negating: "not ($p$ and $q$)" is not "(not $p$) and (not $q$)". Rows where the columns differ are counterexamples.

:::exercise{ref=e15}
:::

## What to take away

- Before dividing, ask whether the divisor can be zero; in a proof, ask it of every symbol.
- An argument by steps needs every step to work, including the first and the smallest.
- Read quantifiers in order. "For every ... there is" lets the second thing depend on the first.
