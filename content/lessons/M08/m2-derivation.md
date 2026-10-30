# Derivation: counting, and probability as counting

## 1. The product and sum rules

**Sum rule.** If a choice can be made in one of two disjoint ways, with $m$ options in the first and $n$ in the second, there are $m + n$ options in all.

**Product rule.** If a choice is made in stages, with $m$ options at the first stage and, whatever was chosen, $n$ at the second, there are $mn$ outcomes. This is M03's $|A \times B| = |A| \cdot |B|$, and it extends to any number of stages: the tree of choices in the widget has $m \times n \times \dots$ leaves.

::::derivation{id=d1 title="Strings with and without repetition"}
:::step
A password of 4 lowercase letters (26 options each, repetition allowed) can be chosen in $26^4 =$ [[456976]] ways.
:::
:::step
If no letter may repeat, the stages have 26, 25, 24 and 23 options, giving [[358800]] passwords.
:::
:::step
An ordering of all $n$ items of a set has $n$ choices first, then $n - 1$, and so on: $n!$ ("$n$ factorial"). A deck of 52 cards has $52!$ orderings, about $8 \times 10^{67}$. The number of orderings of 5 items is [[120]].
:::
::::

**Arrangements.** Choosing $k$ of $n$ items **in order**, without repetition, has $n(n-1)\cdots(n - k + 1) = \dfrac{n!}{(n - k)!}$ outcomes.

## 2. Selections and binomial coefficients

Often order does not matter: a hand of cards, a committee, a mini-batch. Count ordered selections, then divide by how many orders each set appears in. A set of $k$ items appears in exactly $k!$ orders, so the number of **subsets** of size $k$ is

$$
\binom{n}{k} = \frac{n!}{k!\,(n - k)!} ,
$$

read "$n$ choose $k$". These are the **binomial coefficients**.

::::derivation{id=d2 title="Choosing k of n"}
:::step
The number of 2-element subsets of a 5-element set is $\dfrac{5 \cdot 4}{2!} =$ [[10]].
:::
:::step
The number of 5-card hands from a 52-card deck is $\dfrac{52 \cdot 51 \cdot 50 \cdot 49 \cdot 48}{5!} =$ [[2598960]].
:::
:::step
Choosing which $k$ items to take is the same as choosing which $n - k$ to leave, so $\binom{n}{k} = \binom{n}{n - k}$. For instance $\binom{10}{7} = \binom{10}{3} =$ [[120]].
:::
::::

::::predict{id=p3 kind=choice answer=c}
A mini-batch is 4 examples chosen from a dataset of 10, with order irrelevant and no repeats. How many different mini-batches are there?

- $10^4 = 10{,}000$
- $10 \cdot 9 \cdot 8 \cdot 7 = 5{,}040$
- $\binom{10}{4} = 210$
- $4^{10}$

:::reveal
210. The 5,040 ordered selections each list every batch $4! = 24$ times, and $5040/24 = 210$. Allowing repeats and caring about order gives $10^4$. Deciding which of these the problem means is half of every counting problem.
:::
::::

## 3. Pascal's triangle

Here is a way to compute $\binom{n}{k}$ without any division, by an argument about a single item. Fix one item of the $n$. A $k$-subset either contains it (and then picks $k - 1$ of the other $n - 1$) or does not (and picks all $k$ from the other $n - 1$). The two cases are disjoint, so by the sum rule

$$
\binom{n}{k} = \binom{n - 1}{k - 1} + \binom{n - 1}{k} .
$$

Arrange the coefficients in rows $n = 0, 1, 2, \dots$ and each entry is the sum of the two above it: Pascal's triangle.

::::derivation{id=d3 title="Pascal's rule and the row sums"}
:::step
$\binom{5}{2} = \binom{4}{1} + \binom{4}{2} = 4 +$ [[6]].
:::
:::step
Every subset of an $n$-set has some size $k$, so $\sum_k \binom{n}{k}$ counts all subsets, which M03 found to be $2^n$. For $n = 10$ the row sums to [[1024]].
:::
::::

**The binomial theorem.** Expanding $(a + b)^n$ means choosing, from each of the $n$ brackets, either $a$ or $b$, and multiplying. A term $a^k b^{n-k}$ arises once for each way to choose which $k$ brackets give $a$:

$$
(a + b)^n = \sum_{k=0}^{n} \binom{n}{k} a^k b^{n - k} .
$$

::::derivation{id=d4 title="The binomial theorem"}
:::step
The coefficient of $x^2$ in $(1 + x)^5$ is $\binom{5}{2} =$ [[10]].
:::
:::step
Setting $a = b = 1$ gives $\sum_k \binom{n}{k} = 2^n$ again; setting $a = 1$, $b = -1$ gives $\sum_k (-1)^{n-k} \binom{n}{k} = (1 - 1)^n$, which for $n \geq 1$ is [[0]]: subsets of even and odd size are equally many.
:::
::::

:::edge{to=M01 text="counts of arrangements grow past every ladder of powers of ten; their logarithms are what stay manageable."}
:::

## 4. Probability as counting

When an experiment has finitely many **equally likely** outcomes, the probability of an event (a set of outcomes) is

$$
P(E) = \frac{|E|}{|\Omega|} = \frac{\text{favourable outcomes}}{\text{possible outcomes}} ,
$$

where $\Omega$ is the set of all outcomes, the **sample space**. Two dice have $6 \times 6 = 36$ equally likely ordered outcomes; six of them sum to 7, so $P(\text{sum} = 7) = 6/36 = 1/6$. Counting the sample space with the right notion of order is essential: the 21 unordered pairs of dice faces are **not** equally likely (a double appears one way, a mixed pair two ways).

**Complements.** "At least one" is usually easiest through "none": $P(\text{not } E) = 1 - P(E)$.

**Inclusion-exclusion.** For two events, $P(A \cup B) = P(A) + P(B) - P(A \cap B)$: adding counts the overlap twice (M03's count of a union). Adding probabilities is only right for disjoint events.

## 5. The birthday problem

Number the 23 people. The chance that all birthdays differ is the number of ways to give them distinct birthdays over the number of ways to give them any birthdays:

$$
P(\text{all different}) = \frac{365 \cdot 364 \cdots 343}{365^{23}} = \prod_{i=0}^{22} \frac{365 - i}{365} .
$$

::::derivation{id=d5 title="The birthday problem"}
:::step
The chance of at least one shared birthday is [[word:one minus/1 minus/the complement of]] the chance that all differ.
:::
:::step
Using $1 - x \approx e^{-x}$ for small $x$, the product is about $e^{-(0 + 1 + \dots + 22)/365} = e^{-253/365}$, and the exponent's numerator $0 + 1 + \dots + 22 = \binom{23}{2}$ is the number of [[word:pairs]].
:::
:::step
$e^{-253/365} \approx$ [[0.5|tol=0.02]], so a shared birthday has probability about one half; the exact value is 0.507.
:::
::::

The general rule this reveals: among $n$ objects assigned at random to $N$ slots, collisions become likely once $n^2/2$ approaches $N$, that is around $n \approx \sqrt{N}$. With $N = 2^{32}$ possible hash values, collisions start around $2^{16} = 65{,}536$ items: the "birthday bound", which decides how long a hash must be.

:::edge{to=M21 text="probability as counting equally likely outcomes is the special case; M21 builds probability on any sample space, with conditioning and Bayes' rule."}
:::

:::edge{to=M31 text="the union bound, P(A or B) at most P(A) + P(B), returns as the first step of every generalization bound."}
:::

## Summary

| Idea | Count | Use |
| --- | --- | --- |
| Product rule | $m \times n$ | stages of choices |
| Orderings | $n!$ | permutations |
| Ordered selections | $n!/(n - k)!$ | arrangements |
| Subsets | $\binom{n}{k} = n!/(k!\,(n - k)!)$ | hands, committees, batches |
| Pascal | $\binom{n}{k} = \binom{n-1}{k-1} + \binom{n-1}{k}$ | no division needed |
| Probability | favourable over possible, equally likely outcomes | complements for "at least one" |
| Birthday bound | collisions near $n \approx \sqrt{N}$ | hash lengths |
