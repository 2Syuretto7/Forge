# Puzzle: what can you solve for?

A colleague reports two training runs of the same model:

| Run | Learning rate | Batch size | Final loss |
| --- | --- | --- | --- |
| A | 0.1 | 256 | 4.0 |
| B | 0.3 | 512 | 2.5 |

The loss fell by 1.5. Your colleague wants to know how much of that came from the larger learning rate and how much from the larger batch.

Before any symbols, name the unknowns and count the facts.

::::predict{id=p1 kind=choice answer=c}
Assume, generously, that each change contributes a fixed amount to the loss, and that the two contributions simply add. What can you conclude from these two runs?

- The learning rate's effect, but not the batch size's.
- Both effects: two runs give two numbers.
- Only their sum, 1.5. Splitting it needs at least one more run that changes one factor at a time.
- Nothing at all.

:::reveal
Two unknowns (the learning-rate effect $u$ and the batch effect $v$) and one equation, $u + v = 1.5$. Every split, $u = 1.5 - v$ for any $v$, fits the data equally well. The two runs are two numbers, but only their difference carries information about the changes, and that difference is a single equation. A third run that changes only the learning rate gives a second, independent equation and pins both down. This is the heart of the lesson: count unknowns, count independent equations.
:::
::::

## A rectangle

Here is a cleaner case with exactly enough information. A rectangle has perimeter 20 and area 21. What are its sides?

::::predict{id=p2 kind=numeric answer=7 tol=0.01}
What is the length of the longer side?

:::reveal
7 (and the shorter is 3). Calling the sides $x$ and $y$: $2x + 2y = 20$ and $xy = 21$. The first gives $y = 10 - x$; substituting, $x(10 - x) = 21$, so $x^2 - 10x + 21 = 0$, which factors as $(x - 3)(x - 7) = 0$. Two unknowns, two independent equations, and a quadratic in the middle: everything this lesson builds.
:::
::::

## An equation is a balance

An equation says two expressions have equal value. The picture that makes every algebra rule obvious is a balance: the two sides are pans, and the equation says the beam is level. You may do anything to one pan as long as you do exactly the same to the other. Try values of $x$ until the beam levels, then read the steps the widget takes to solve the equation directly.

:::widget{name=BalanceScale a=3 b=2 c=1 d=8}
:::

Now set $a$ equal to $c$. The steps reach a point where they would divide by zero. What does the balance tell you then?

## Questions to carry into the derivation

1. Which manipulations keep an equation true, and why exactly those?
2. How do you solve two equations in two unknowns, and when is that impossible?
3. Why does multiplying an inequality by a negative number flip it?
4. Where does the quadratic formula come from?
