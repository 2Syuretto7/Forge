# Derivation: logic, sets, functions and proof

## 1. Propositions and connectives

A **proposition** is a statement that is true or false. Write $T$ and $F$. From propositions $p$ and $q$ build new ones:

| $p$ | $q$ | not $p$ | $p$ and $q$ | $p$ or $q$ | $p \Rightarrow q$ |
| --- | --- | --- | --- | --- | --- |
| T | T | F | T | T | T |
| T | F | F | F | T | F |
| F | T | T | F | T | T |
| F | F | T | F | F | T |

"Or" is inclusive: true when either or both hold. The **implication** $p \Rightarrow q$ ("if $p$ then $q$") is false in exactly one row: $p$ true and $q$ false. That is the only way to break a promise "if $p$, then $q$". When $p$ is false, the promise was never tested, and logic counts it as kept. This feels odd at first; it is what makes the rest of mathematics work, because "for every $n$, if $n$ is even then $n^2$ is even" must be true even though most $n$ are odd.

::::derivation{id=d1 title="Implication, converse and contrapositive"}
:::step
In the row where $p$ is true and $q$ is false, $p \Rightarrow q$ is [[word:false/F]].
:::
:::step
So of the four rows, the number in which $p \Rightarrow q$ is true is [[3]].
:::
:::step
The **contrapositive** (not $q$) $\Rightarrow$ (not $p$) is false only when not $q$ is true and not $p$ is false, that is when $q$ is false and $p$ is [[word:true/T]]. That is the same single row, so a statement and its contrapositive are logically equivalent.
:::
:::step
The **converse** $q \Rightarrow p$ is false when $q$ is true and $p$ is false. Counting the rows where $p \Rightarrow q$ and $q \Rightarrow p$ disagree gives [[2]], so the converse is a different statement.
:::
::::

Two statements are **logically equivalent** when their truth tables agree in every row. Equivalences worth knowing: the contrapositive; $p \Rightarrow q$ is equivalent to (not $p$) or $q$; and De Morgan's laws, not ($p$ and $q$) $\equiv$ (not $p$) or (not $q$), and not ($p$ or $q$) $\equiv$ (not $p$) and (not $q$).

## 2. Quantifiers

A predicate $P(x)$ becomes a statement when you quantify it:

- $\forall x\, P(x)$, "for every $x$, $P(x)$": true when $P$ holds for each $x$ in the domain.
- $\exists x\, P(x)$, "there exists $x$ with $P(x)$": true when at least one $x$ works.

Negation swaps them. "Not every swan is white" means "some swan is not white":

$$
\text{not}\ \forall x\, P(x) \;\equiv\; \exists x\ \text{not}\ P(x), \qquad \text{not}\ \exists x\, P(x) \;\equiv\; \forall x\ \text{not}\ P(x) .
$$

This is the logic of counterexamples: to refute "for every", exhibit one.

The **order** of quantifiers matters. Over the integers:

- $\forall x\, \exists y\ (y > x)$: every integer has a bigger one. True: take $y = x + 1$, which depends on $x$.
- $\exists y\, \forall x\ (y > x)$: some integer is bigger than every integer. False: no $y$ beats $y + 1$.

The words are the same; only the order differs, and with it, whether $y$ may depend on $x$.

::::derivation{id=d2 title="Negating and ordering quantifiers"}
:::step
The negation of "every model in the zoo has fewer than a billion parameters" is "[[word:some/at least one/there exists a]] model in the zoo has a billion parameters or more".
:::
:::step
To refute a claim of the form "for every $n \leq 1000$, $P(n)$", the number of counterexamples you need is [[1]].
:::
:::step
To prove a claim of the form "there exists $n$ with $P(n)$", the number of examples you need is also [[1]]; proving "for every" takes an argument, not examples.
:::
:::step
Of "$\forall x\, \exists y$ ($y$ is the mother of $x$)" and "$\exists y\, \forall x$ ($y$ is the mother of $x$)", the one that is true among all people is the [[word:first/1st/former]].
:::
::::

::::predict{id=p3 kind=choice answer=a}
A claim about a trained model reads: "for every input $x$ there is a perturbation $\delta$ of size at most 0.01 such that the model's prediction on $x + \delta$ is wrong." Which statement is stronger (implies the other)?

- "There is one perturbation $\delta$ of size at most 0.01 that makes the prediction wrong for every input $x$."
- The original statement.
- They are equivalent.

:::reveal
"There is one $\delta$ for every $x$" ($\exists \delta\, \forall x$) implies "for every $x$ there is a $\delta$" ($\forall x\, \exists \delta$): if one $\delta$ works for all inputs, then each input certainly has one. The reverse fails, because in the original each input may need its own perturbation. In the machine-learning literature the stronger one is called a universal adversarial perturbation, and it is a much more surprising finding.
:::
::::

## 3. Sets

A **set** is a collection of distinct objects, its **elements**. Write $x \in A$ for "$x$ is an element of $A$". Order and repetition do not matter: $\{1, 2\} = \{2, 1, 1\}$.

- $A \subseteq B$ ($A$ is a **subset** of $B$): every element of $A$ is in $B$. Two sets are equal when each is a subset of the other.
- $A \cup B$ (**union**): elements in $A$ or $B$. $A \cap B$ (**intersection**): elements in both. $A \setminus B$ (**difference**): in $A$ but not $B$.
- $A \times B$ (**Cartesian product**): all ordered pairs $(a, b)$ with $a \in A$ and $b \in B$.
- The **power set** of $A$: the set of all subsets of $A$, including the empty set $\varnothing$ and $A$ itself.

The connectives and the set operations are the same thing seen twice: $x \in A \cup B$ means ($x \in A$) or ($x \in B$), and De Morgan's laws become $(A \cup B)^c = A^c \cap B^c$.

::::derivation{id=d3 title="Counting with sets"}
:::step
Counting $A \cup B$ by adding $|A| + |B|$ counts the elements of $A \cap B$ twice. With $|A| = 10$, $|B| = 7$ and $|A \cap B| = 3$, the union has [[14]] elements.
:::
:::step
$A \times B$ pairs each of the $|A|$ elements with each of the $|B|$, so with $|A| = 10$ and $|B| = 7$ it has [[70]] pairs.
:::
:::step
Building a subset of a 5-element set means deciding, for each element, in or out: $2 \times 2 \times 2 \times 2 \times 2$, so the power set has [[32]] elements.
:::
::::

## 4. Functions as sets of pairs

A **function** $f: A \to B$ assigns to each element of the **domain** $A$ exactly one element of the **codomain** $B$. Made precise, $f$ is a set of pairs $(a, b) \in A \times B$ in which every $a \in A$ appears exactly once as a first entry. Nothing about formulas is required; a lookup table is a function.

- $f$ is **injective** (one-to-one) if different inputs give different outputs.
- $f$ is **surjective** (onto) if every element of $B$ is some output.
- $f$ is **bijective** if both; then it has an inverse.

How many functions are there from a 3-element set to a 2-element set? Each of the 3 inputs independently picks one of 2 outputs: $2^3 = 8$. In general $|B|^{|A|}$. That is why the set of all functions from $A$ to $B$ is sometimes written $B^A$.

:::edge{to=M08 text="sets, products and functions become the objects you count: outcomes, arrangements and selections."}
:::

## 5. Four ways to prove a statement

**Direct proof.** Assume the hypothesis, reason forward to the conclusion. *Claim:* the sum of two even numbers is even. *Proof:* write them $2a$ and $2b$; their sum is $2(a + b)$, which is even.

**Proof by contrapositive.** To prove $p \Rightarrow q$, prove (not $q$) $\Rightarrow$ (not $p$), which is equivalent.

::::derivation{id=d4 title="If n squared is even, then n is even"}
:::step
The contrapositive is: if $n$ is odd then $n^2$ is odd. Write an odd $n$ as $2k + 1$. Then $n^2 = 4k^2 + 4k + 1 = 2(\,?\,) + 1$, where the bracket is [[2*k^2 + 2*k]].
:::
:::step
A number of the form $2m + 1$ with $m$ an integer is [[word:odd]], so the contrapositive holds, and with it the original statement.
:::
::::

**Proof by contradiction.** Assume the statement is false and derive something impossible. Then the assumption was wrong.

::::derivation{id=d5 title="The square root of 2 is irrational"}
:::step
Suppose $\sqrt{2} = p/q$ with integers $p, q$ and the fraction in lowest terms (no common factor). Squaring, $p^2 = 2q^2$, so $p^2$ is even, and by the previous derivation $p$ is [[word:even]].
:::
:::step
Write $p = 2k$. Then $4k^2 = 2q^2$, so $q^2 =$ [[2*k^2]].
:::
:::step
So $q^2$ is even and $q$ is even too. Then $p$ and $q$ share the factor [[2]], contradicting lowest terms. So no such fraction exists.
:::
::::

**Proof by counterexample.** To prove that a "for every" statement is false, exhibit one case. $n = 40$ disproved Euler's pattern.

A fifth method, **induction**, proves statements about every whole number by a domino argument. You will meet a broken version of it in Movement 5 and the real thing in M05.

:::edge{to=M05 text="induction proves a statement for every whole number at once, the way a row of dominoes falls."}
:::

:::edge{to=M31 text="quantifiers return in generalization bounds, which must hold for every model in a class at once, and proof by contradiction powers their proofs."}
:::

## Summary

| Idea | Precise form | Remember |
| --- | --- | --- |
| Implication | false only when $p$ true, $q$ false | equivalent to its contrapositive, not its converse |
| Negating quantifiers | not $\forall$ = $\exists$ not | one counterexample refutes "for every" |
| Quantifier order | $\exists y\, \forall x$ implies $\forall x\, \exists y$ | not the other way |
| Sets | union, intersection, product, power set | $\lvert A \cup B \rvert = \lvert A \rvert + \lvert B \rvert - \lvert A \cap B \rvert$ |
| Functions | a set of pairs, each input once | $\lvert B \rvert^{\lvert A \rvert}$ functions from $A$ to $B$ |
| Proof | direct, contrapositive, contradiction, counterexample | testing is evidence, not proof |
