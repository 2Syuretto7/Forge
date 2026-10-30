# Break it: illegal divisions, squared inequalities and planted errors

Every rule in Section 2 has a condition. This movement breaks each condition on purpose and watches what fails. Predict before you run.

## Dividing by something that can be zero

:::exercise{ref=e13}
:::

## Squaring both sides of an inequality

$2 < 3$ and $4 < 9$. Is it always safe to square both sides of an inequality?

::::predict{id=p5 kind=choice answer=c}
For which pairs with $a < b$ does $a^2 < b^2$ fail?

- Never: squaring is increasing.
- Only when $a$ and $b$ are both negative.
- Whenever $|a| \geq |b|$, which needs $a$ negative: for example $-3 < 2$ but $9 > 4$.
- Only when $a = b$.

:::reveal
Squaring keeps the order only for non-negative numbers. $a^2 < b^2$ means $|a| < |b|$, and $a < b$ does not imply that when $a$ is negative. Both negative is one way to fail ($-3 < -2$ but $9 > 4$), but a negative $a$ and a positive $b$ with $|a| \geq |b|$ fails too. A random search finds such pairs within a few tries.
:::
::::

:::exercise{ref=e14}
:::

## A derivation with two planted errors

Below is the balance once more. Set it to $x^2 = 4x$ in your head: the balance can only hold linear sides, which is a reminder that the widget, like any rule, has a domain where it applies.

:::widget{name=BalanceScale a=2 b=0 c=2 d=0}
:::

With $a = c$ and $b = d$, every $x$ balances: the equation $2x = 2x$ says nothing. Now find the broken steps in a longer chain, using the checker from the build movement.

:::exercise{ref=e15}
:::

## What to take away

- Before dividing by an expression, ask whether it can be zero. If it can, factor instead.
- Squaring, square roots and multiplying by an unknown sign do not preserve inequalities.
- A random-point check is cheap and catches almost every wrong step. Use it on your own algebra.
