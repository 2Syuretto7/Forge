# Scale: fifty claims and a long race

A hunter is only as good as its search. This movement runs it over fifty classic claims, half of them false, and records how long each falsehood survived. Then it follows one claim that is true for every number below 26,861.

## Fifty claims

::::predict{id=p4 kind=choice answer=c}
The hunter checks each false claim on $n = 0, 1, 2, \dots$ up to a limit. What do you expect about the number of cases each false claim survives?

- About the same for all of them: falsehood shows up quickly or never.
- Most survive thousands of cases.
- Most break within the first few cases, but a few survive for a long time: a long tail.

:::reveal
Most false claims break almost at once (the first even prime, the first odd non-prime), which is why quick tests are so useful. But a few survive a long time: Euler's polynomial survives 40 cases and Fermat's guess that $2^{2^n} + 1$ is always prime survives five, each case vastly larger than the one before. The long tail is exactly why surviving a test is not proof.
:::
::::

:::exercise{ref=e10}
:::

:::exercise{ref=e11}
:::

## A race that turns after 26,861

Divide the primes by 4: every odd prime leaves remainder 1 or 3. Count, up to $n$, how many leave each. The remainder-3 primes lead at $n = 3$, at $n = 100$, at $n = 10{,}000$. "The remainder-3 primes are never behind" survives tens of thousands of tests, and is false.

:::exercise{ref=e12}
:::

The widget lets you compare the laws you are relying on. Every row of a truth table is a case, and a finite table can be checked completely: for statements about finitely many true-or-false inputs, testing every case **is** a proof. It is the infinite cases that need arguments.

:::widget{name=TruthTable pair=distribute}
:::
