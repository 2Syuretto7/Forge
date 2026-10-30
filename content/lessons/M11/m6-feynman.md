# Explain it plainly: rank as information

Explain what rank means in terms of the information in a set of measurements.

Guidelines:

- Write 150 to 400 words.
- Use sensors or survey questions as the picture.
- Say what a repeated or combined measurement adds.
- Say what the missing rank means for the unknowns.

:::feynman{id=f1 prompt="Explain what rank means in terms of the information in the data." key_points="The rank is the number of independent measurements, rows that are not combinations of other rows|A measurement that is a combination of others adds no new information, like a sensor that reads twice what another reads|The same number counts independent columns, the distinct effects the unknowns have on the readings|When the rank is below the number of unknowns, some combinations of the unknowns cannot be determined from the data at all|In floating point the rank depends on a tolerance, because nearly repeated measurements add almost no information"}
:::

## A written proof

:::feynman{id=proof1 prompt="Prove the rank-nullity theorem: for an m by n matrix A, rank(A) + dim null(A) = n." key_points="Row operations are invertible, so they change neither the null space nor the number of independent columns|In row echelon form the rank r is the number of pivot columns, and the other n - r columns are free|Setting one free variable to 1 and the others to 0 and back substituting gives one null-space vector per free column|These vectors are independent, since each has a 1 in its own free position where the others have 0|They span the null space, because every solution of Ax = 0 is determined by the values of its free variables, so dim null(A) = n - r"}
:::
