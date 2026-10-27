# Explain it plainly: the SVD

You have derived the SVD, built it, and broken it. Now explain it to someone who has never seen a matrix decomposition. If you cannot make it simple, find the step you are hiding behind notation and work it out again.

Guidelines:

- Write 150 to 400 words.
- Use a concrete example: a specific $2 \times 2$ matrix, an image, a dataset of points.
- Explain why it works, not only what the pieces are called.
- Avoid unexplained jargon. "Orthonormal" needs a plain-language meaning if you use it.

:::feynman{id=f1 prompt="Explain what the singular value decomposition of a matrix is, why every matrix has one, and why keeping only the largest singular values gives a good compressed version of the matrix." key_points="A matrix acts on vectors by rotating and stretching; the SVD splits that action into rotate, stretch along perpendicular axes, rotate|The singular values are the stretch factors, and the singular vectors are the input and output directions that get stretched|The SVD can be built from the eigenvectors of A transpose A, whose eigenvalues are the squared singular values|The matrix is a sum of rank-one pieces ordered by singular value|Dropping the pieces with small singular values loses only the sum of their squares, and no other matrix of the same rank does better"}
:::

When you are done, compare your text against the key points in the rubric. The grader will quote phrases it believes are wrong; treat each quote as a pointer to a step you should re-derive.
