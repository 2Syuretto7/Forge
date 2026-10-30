# Capstone: a robust linear solver

Write `solve(A, b)` that never crashes and never lies. For any matrix (square, tall, wide, singular, nearly singular, with rows in any order) it reports the numerical rank, whether the system has no solution, exactly one or infinitely many, a solution when one exists, and the residual $\|Ax - b\|$. Forty test systems, each with a known answer, check it.

:::exercise{ref=capstone}
:::

## When you finish

Your solver answers "no solution" honestly. M12 asks for the next best thing, the $x$ whose $Ax$ is nearest to $b$, and finds that the residual of that best fit is perpendicular to every column. M26 returns to pivoting as the first lesson in numerical stability.

:::edge{to=M12 text="no exact solution: least squares finds the nearest point of the column space."}
:::
