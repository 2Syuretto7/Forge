# Explain it plainly: order matters

Explain, with two moves on a sheet of paper, why $AB$ is usually not $BA$.

Guidelines:

- Write 150 to 400 words.
- Use one rotation and one stretch you could do to a real sheet.
- Say what "do $B$ first" means for the product $AB$.
- Give one pair of moves that do commute.

:::feynman{id=f1 prompt="Explain why AB is usually not BA, using two moves on a sheet of paper." key_points="The product AB means do B first and then A|Take a rotation by a quarter turn and a stretch along one edge of the sheet|Rotating first puts the other edge along the stretching direction, so a different edge gets longer|The two orders give different sheets, so the matrices differ|Some pairs commute, such as two rotations or stretching everything by the same factor, but that is the exception"}
:::

## A written proof

:::feynman{id=proof1 prompt="Prove that the matrix of the composition x -> A(Bx) has entries (AB)_ij = sum over k of A_ik B_kj, and deduce that matrix multiplication is associative." key_points="Column j of the matrix of a linear map is the image of the basis vector e_j|B sends e_j to its column j, which is the sum over k of B_kj e_k|By linearity A sends that to the sum over k of B_kj times column k of A|Entry i of that vector is the sum over k of A_ik B_kj|Composition of functions is associative, so (AB)C and A(BC) are the matrix of the same map and are equal"}
:::
