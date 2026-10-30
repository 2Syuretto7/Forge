# Explain it plainly: rotate, stretch, rotate

Explain why any linear map is a rotation, a stretch and another rotation.

Guidelines:

- Write 150 to 400 words.
- Use a circle drawn on a rubber sheet as the picture.
- Say what the singular values are in that picture.
- Say what a zero singular value does.

:::feynman{id=f1 prompt="Explain why any linear map is a rotation, a stretch and another rotation." key_points="The SVD writes the map as U times Sigma times V transpose|The first rotation turns a special pair of perpendicular input directions onto the axes|The stretch scales each axis by its own singular value without turning anything|The second rotation turns the stretched axes to their output directions, which are again perpendicular|So every map turns a circle into an ellipse whose axes are the singular values, and a zero singular value flattens one axis completely"}
:::

## A written proof

:::feynman{id=proof1 prompt="Prove that every real m by n matrix A has a singular value decomposition A = U Sigma V^T with orthonormal U and V and a nonnegative diagonal Sigma, by constructing it from the eigen-decomposition of A^T A." key_points="A^T A is symmetric, so by the spectral theorem A^T A = V Lambda V^T with orthonormal V|Each eigenvalue is nonnegative because lambda_i = v_i^T A^T A v_i = ||A v_i||^2|Defines sigma_i as the square root of lambda_i and u_i = A v_i / sigma_i when sigma_i > 0|Shows the u_i are orthonormal: u_i . u_j = lambda_j (v_i . v_j) / (sigma_i sigma_j)|Concludes A v_i = sigma_i u_i for every i (A v_i = 0 when sigma_i = 0), completes the u_i to an orthonormal basis, and so A V = U Sigma, that is A = U Sigma V^T"}
:::
