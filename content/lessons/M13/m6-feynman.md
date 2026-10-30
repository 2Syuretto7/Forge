# Explain it plainly: eigenvectors

Explain what an eigenvector is to someone who has never seen a matrix.

Guidelines:

- Write 150 to 400 words.
- Use a physical transformation: stretching a rubber sheet, a lens, a recipe applied again and again.
- Say what the eigenvalue is.
- Say what happens when the transformation is repeated many times.

:::feynman{id=f1 prompt="Explain what an eigenvector is to someone who has never seen a matrix." key_points="A transformation moves every arrow, and most arrows change direction|An eigenvector is a direction the transformation does not turn: arrows along it are only stretched, shrunk or flipped|The eigenvalue is the factor by which arrows along that direction are stretched|Repeating the transformation many times pulls almost every starting arrow toward the direction with the largest stretch|A concrete example such as a rubber sheet stretched sideways, where the horizontal and vertical directions keep their direction"}
:::

## A written proof

:::feynman{id=proof1 prompt="Prove that a real symmetric matrix has real eigenvalues, and that its eigenvectors for different eigenvalues are orthogonal." key_points="Computes v1 . S v2 in two ways, using S v2 = l2 v2 on one side and S^T = S with S v1 = l1 v1 on the other|Concludes (l1 - l2)(v1 . v2) = 0, so v1 . v2 = 0 when l1 differs from l2|For realness, takes S v = l v with v possibly complex and considers conj(v)^T S v|Shows that number equals its own complex conjugate because S is real and symmetric|Since it also equals l times the squared length of v, which is real and positive, l is real"}
:::
