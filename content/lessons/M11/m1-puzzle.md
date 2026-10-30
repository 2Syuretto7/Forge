# Puzzle: three sensors, and the solver says singular

Three sensors each read a weighted sum of three unknown loads $x_1, x_2, x_3$:

$$
\begin{aligned}
x_1 + 2x_2 + x_3 &= 4 \\
2x_1 + 4x_2 + 2x_3 &= 8 \\
x_1 + x_3 &= 2
\end{aligned}
$$

You hand the system to a solver and it refuses: the matrix is singular.

::::predict{id=p1 kind=choice answer=b}
Why does the solver refuse?

- The right-hand sides are too large.
- The second sensor reads exactly twice the first, so it adds no information: two independent equations for three unknowns.
- The third equation is missing $x_2$.
- Every system with three unknowns needs four sensors.

:::reveal
The second row is twice the first, readings included. It repeats what the first sensor said, so there are only two independent equations, and one combination of the loads stays undetermined. Section 4 calls the number of independent rows the **rank**: here 2, below the 3 unknowns, so there are infinitely many solutions. Missing $x_2$ is harmless; a repeated sensor is not.
:::
::::

::::predict{id=p2 kind=numeric answer=1 tol=0.01}
How many free parameters does the family of solutions have?

:::reveal
One. Three unknowns minus two independent equations leaves one. Indeed $x = (2, 1, 0) + t\,(-1, 0, 1)$ solves the system for every $t$: the direction $(-1, 0, 1)$ is invisible to all three sensors, since each reads $x_1$ and $x_3$ with equal weight. The **rank-nullity theorem** of Section 5 says the count always works out this way.
:::
::::

Step through the elimination. With the second preset the second row becomes all zeros: the redundancy shows itself. Switch to the third preset, where the second sensor's reading is slightly off, and the zero row demands $0 = $ something nonzero.

:::widget{name=EliminationStepper preset=same}
:::

## Questions to carry into the derivation

1. Which operations on equations keep their solutions?
2. How can you tell from the numbers alone that a row repeats information?
3. When does $Ax = b$ have no solution, exactly one, or infinitely many?
4. Why does the order in which rows are used matter on a computer but not on paper?
