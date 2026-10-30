# Derivation: the rules of the game, and solving for unknowns

Algebra has a reputation for tricks. It has none. Every legal move comes from a short list of rules about numbers, and this movement derives every technique from that list.

## 1. Variables are names for numbers

A **variable** such as $x$ is a name for a number you do not know yet (or a number that can vary). An **expression** such as $3x + 2$ combines variables and numbers with the operations. An **equation** such as $3x + 2 = 11$ claims two expressions are equal, and **solving** it means finding every value of the variable that makes the claim true.

Because $x$ stands for a number, everything true of all numbers is true of $x$. That is the entire foundation.

## 2. The rules of arithmetic

For all real numbers $a$, $b$, $c$:

| Rule | For addition | For multiplication |
| --- | --- | --- |
| Commutative | $a + b = b + a$ | $ab = ba$ |
| Associative | $(a + b) + c = a + (b + c)$ | $(ab)c = a(bc)$ |
| Identity | $a + 0 = a$ | $a \cdot 1 = a$ |
| Inverse | $a + (-a) = 0$ | $a \cdot \frac{1}{a} = 1$, only if $a \neq 0$ |
| Distributive | $a(b + c) = ab + ac$ | |

A set of numbers with operations obeying these rules is called a **field**; the rationals and the reals are fields, and so are the complex numbers you will meet in M07. Subtraction is adding the inverse, $a - b = a + (-b)$, and division is multiplying by the inverse, $a / b = a \cdot \frac{1}{b}$.

Notice the one exception: zero has no multiplicative inverse. Nothing times zero is one. Almost every mistake in algebra is, somewhere, a division by something that can be zero.

**Doing the same to both sides.** If $A = B$ are equal numbers, then $A + c = B + c$ and $A c = B c$, because an operation applied to equal inputs gives equal outputs. That is all "do the same to both sides" means. The reverse direction is the subtle one: from $A c = B c$ you may conclude $A = B$ only by multiplying by $1/c$, which needs $c \neq 0$.

## 3. Linear equations

An equation $a x + b = c$ with $a \neq 0$ is **linear** in $x$: $x$ appears only multiplied by a number. Solve it using only the rules.

::::derivation{id=d1 title="Solving a linear equation from the rules"}
:::step
Start from $3x + 2 = 11$. Add $-2$ to both sides. The left becomes $3x + (2 + (-2)) = 3x + 0 = 3x$, so $3x =$ [[9]].
:::
:::step
Multiply both sides by $\frac{1}{3}$. The left becomes $\left(\frac{1}{3} \cdot 3\right) x = 1 \cdot x = x$, so $x =$ [[3]].
:::
:::step
In general, $a x + b = c$ with $a \neq 0$ gives $x =$ [[(c - b)/a]].
:::
:::step
If $a = 0$ the equation reads $b = c$: true for every $x$ when $b = c$, and for no $x$ when $b \neq c$. How many solutions does $0 \cdot x + 2 = 5$ have? [[0]]
:::
::::

Every step used one named rule. Writing out each rule is slow, and you will stop doing it within a week; the point is to know that you could, which is what lets you trust a manipulation you have never seen before.

## 4. Two equations in two unknowns

Two unknowns need two equations, and they must be **independent**: the second must say something the first does not. There are two classical methods.

**Substitution:** solve one equation for one unknown, substitute into the other. From $x + y = 10$, $y = 10 - x$; then $x - y = 4$ becomes $x - (10 - x) = 4$, so $2x = 14$.

**Elimination:** add or subtract multiples of the equations to remove an unknown. Adding $x + y = 10$ and $x - y = 4$ removes $y$ at once: $2x = 14$. Elimination is the method that scales; in M11 it becomes Gaussian elimination on systems of thousands of equations.

Do elimination once in general:

$$
\begin{aligned}
a x + b y &= p \\
c x + d y &= q
\end{aligned}
$$

Multiply the first equation by $d$ and the second by $b$, and subtract: the $y$ terms cancel, leaving $(ad - bc)\,x = pd - bq$.

::::derivation{id=d2 title="Elimination, and the number that decides everything"}
:::step
For $x + y = 10$ and $x - y = 4$, adding the equations gives $2x = 14$, so $x =$ [[7]].
:::
:::step
Then $y = 10 - x =$ [[3]].
:::
:::step
In general, $(ad - bc)\,x = pd - bq$, so when $ad - bc \neq 0$, $x =$ [[(p*d - b*q)/(a*d - b*c)]].
:::
:::step
The number $ad - bc$ is called the **determinant**. For the system $2x + 4y = 6$, $x + 2y = 3$, it equals $2 \cdot 2 - 4 \cdot 1 =$ [[0]], and the second equation is the first divided by 2: not independent.
:::
::::

When the determinant is zero, the two equations describe parallel lines (no solution) or the same line (infinitely many). When it is small but not zero, the lines are nearly parallel, and their crossing point slides a long way when either line moves slightly. You will measure exactly how far in Movement 4.

:::edge{to=M11 text="elimination on two equations becomes Gaussian elimination on many, and the determinant becomes the question of rank."}
:::

:::edge{to=M12 text="two equations in two unknowns return as the normal equations of least squares, which fit a line to many points at once."}
:::

## 5. Inequalities

An **inequality** $A < B$ says $B - A$ is positive. Adding the same number to both sides keeps $B - A$ unchanged, so it is safe. Multiplying by a positive $c$ multiplies $B - A$ by $c$, which keeps it positive. Multiplying by a negative number is different.

::::derivation{id=d3 title="Why a negative multiplier flips an inequality"}
:::step
Suppose $a < b$, so $b - a > 0$. Then $(-a) - (-b) = b - a$, which is positive, so $-a$ is [[word:greater/bigger/larger]] than $-b$.
:::
:::step
So multiplying both sides by $-1$ reverses the inequality. Solving $-2x < 6$: multiply by $-\frac{1}{2}$ and flip, giving $x > $ [[-3]].
:::
:::step
The **absolute value** $|x|$ is $x$ if $x \geq 0$ and $-x$ otherwise: the distance from $x$ to 0. So $|x - 3| < 2$ says $x$ is within 2 of 3, which is $1 < x <$ [[5]].
:::
::::

::::predict{id=p3 kind=choice answer=b}
Someone solves $x^2 = 4x$ by dividing both sides by $x$, getting $x = 4$. What went wrong?

- Nothing: $x = 4$ is the only solution.
- A solution was lost: $x = 0$ also works, and dividing by $x$ assumed $x \neq 0$.
- They should have taken square roots instead, giving $x = 2$.
- The equation has no solutions.

:::reveal
$x = 0$ satisfies $0 = 0$. Dividing by $x$ multiplies by $1/x$, which exists only when $x \neq 0$, so the step silently assumed the very thing that excludes a solution. The safe move is to bring everything to one side and factor: $x^2 - 4x = x(x - 4) = 0$, and a product is zero exactly when one of its factors is zero.
:::
::::

That last fact deserves its name. **The zero-product rule:** if $AB = 0$ then $A = 0$ or $B = 0$. Proof: if $A \neq 0$, multiply both sides by $1/A$ to get $B = 0$.

## 6. Quadratic equations

A **quadratic** equation has the form $a x^2 + b x + c = 0$ with $a \neq 0$. When it factors (as $x^2 - 10x + 21 = (x - 3)(x - 7)$ did in the puzzle), the zero-product rule finishes the job. When it does not, **completing the square** always works. The idea: $(x + p)^2 = x^2 + 2px + p^2$, so any $x^2 + 2px$ is one square minus $p^2$.

::::derivation{id=d4 title="Completing the square, and the quadratic formula"}
:::step
$x^2 + 6x + 5 = 0$. Since $(x + 3)^2 = x^2 + 6x + 9$, the equation is $(x + 3)^2 - 9 + 5 = 0$, that is $(x + 3)^2 =$ [[4]].
:::
:::step
So $x + 3 = \pm 2$, and the two solutions are $x = -1$ and $x =$ [[-5]].
:::
:::step
In general, divide $a x^2 + b x + c = 0$ by $a$ and complete the square with $p = \frac{b}{2a}$: $\left(x + \frac{b}{2a}\right)^2 = \frac{b^2 - 4ac}{4a^2}$. Taking square roots, the larger solution is $x =$ [[(-b + sqrt(b^2 - 4*a*c))/(2*a)]] when $a > 0$.
:::
:::step
The quantity $D = b^2 - 4ac$ is the **discriminant**. A square is never negative, so when $D < 0$ the number of real solutions is [[0]].
:::
::::

The **quadratic formula** $x = \dfrac{-b \pm \sqrt{b^2 - 4ac}}{2a}$ is nothing but completing the square once, in general, so that you never have to do it again. Its derivation also explains its parts: $-\frac{b}{2a}$ is the centre of the parabola, and $\frac{\sqrt{D}}{2a}$ is how far each root sits from that centre.

## 7. How do you know a step is right?

Every manipulation should produce an expression with the same value as the one before, for every value of the variables where both make sense. That suggests a mechanical check: pick random values for the variables and evaluate both sides. If they disagree anywhere, the step is wrong, and the disagreeing values are a **counterexample**. If they agree at fifty random points, the step is very probably right.

"Very probably" is not "certainly". Two different polynomials of low degree can agree only at a few points, so random points almost never land on all of them; that makes the check powerful in practice. But it is evidence, not proof, and M03 is about the difference.

:::edge{to=M03 text="testing at random points finds counterexamples but never proves a claim; M03 says what a proof adds."}
:::

## Summary

| Idea | Statement | Watch out for |
| --- | --- | --- |
| Same to both sides | $A = B \Rightarrow A + c = B + c$, $Ac = Bc$ | undoing a multiplication needs $c \neq 0$ |
| Linear equation | $ax + b = c \Rightarrow x = (c - b)/a$ | $a = 0$: none or all |
| Two unknowns | eliminate; $x = (pd - bq)/(ad - bc)$ | determinant $ad - bc = 0$ |
| Inequalities | multiplying by a negative flips them | squaring both sides |
| Zero product | $AB = 0 \Rightarrow A = 0$ or $B = 0$ | dividing by a variable |
| Quadratic formula | $x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$ | $D < 0$: no real roots |
