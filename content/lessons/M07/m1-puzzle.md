# Puzzle: turning twice

Take the point $(1, 0)$ on a sheet of paper and turn the paper about the origin by 30 degrees, then by 45 degrees.

::::predict{id=p1 kind=choice answer=a}
Is that the same as one turn by 75 degrees?

- Yes, always: turns about the same point add.
- Only approximately; small errors accumulate.
- No: a turn changes the axes, so the second turn is measured differently.

:::reveal
Yes, exactly. Turns about the same point compose by adding angles, and they commute: 30 then 45 is 45 then 30. That makes rotations unusually well behaved among machines (M04 found that most compositions do not commute). The rest of this lesson finds a kind of number whose multiplication is exactly this adding of angles.
:::
::::

::::predict{id=p2 kind=numeric answer=0.866 tol=0.01}
After turning $(1, 0)$ by 30 degrees, what is the point's horizontal coordinate?

:::reveal
$\cos 30^\circ = \sqrt{3}/2 \approx 0.866$, and the vertical coordinate is $\sin 30^\circ = 0.5$. Sine and cosine are exactly the coordinates of a turned point. A 30-60-90 triangle with hypotenuse 1 has sides 0.5 and $\sqrt{1 - 0.25} = 0.866$, by Pythagoras.
:::
::::

The widget turns two arrows, $z$ and $w$, and multiplies them. Watch the product's angle and length as you move the sliders.

:::widget{name=UnitCircle theta=30 phi=45}
:::

## Questions to carry into the derivation

1. Why does the hypotenuse satisfy $c^2 = a^2 + b^2$?
2. What exactly are sine and cosine, and why measure angles in radians?
3. What are the formulas for $\cos(\alpha + \beta)$ and $\sin(\alpha + \beta)$, and where do they come from?
4. What kind of number turns when you multiply by it?
