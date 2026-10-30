# Scale: ten thousand systems, and the first sight of conditioning

One two-by-two system is a puzzle. Ten thousand random ones are a population, and populations have shapes. This movement solves them all at once with NumPy and asks how many are dangerous.

## Solving many systems at once

NumPy can apply the elimination formula to whole arrays at once: `a`, `b`, `c` and `d` become arrays of length 10,000, and one line computes every determinant.

:::exercise{ref=e10}
:::

## Nearly parallel lines

::::predict{id=p4 kind=choice answer=b}
You draw 10,000 random systems with all four coefficients uniform between $-1$ and $1$. About how many have a determinant smaller than $0.01$ in absolute value?

- None, or a handful: a determinant that small needs a coincidence.
- About 200, roughly 2 percent.
- About 2,000.
- About half of them.

:::reveal
About 200. For small thresholds $t$ the fraction with $|ad - bc| < t$ is close to $2t$, so $t = 0.01$ catches about 2 percent. Nearly singular systems are not exotic: in any large collection of equations some will be close to parallel, and on those a tiny error in the right-hand side moves the solution a long way.
:::
::::

The widget shows what a two-by-two matrix does to the plane. Its determinant is the factor by which it scales areas. Drag $d$ toward $bc/a$: the square flattens toward a line, the determinant heads to zero, and the condition number (which you will meet properly in M14) shoots up.

:::widget{name=MatrixTransform a=1 b=0.9 c=1 d=1}
:::

:::exercise{ref=e11}
:::

## Many points, two unknowns

Two points determine a line: two equations, two unknowns. Fifty noisy points do not lie on any line. Which two should you trust?

:::exercise{ref=e12}
:::

The answer, "none of them in particular, use all fifty", is least squares, and it arrives in M12 as two equations in two unknowns of exactly the kind you solved today.
