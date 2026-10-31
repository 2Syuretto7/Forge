# Explain it plainly: why ellipses

Explain why the contours of a 2D Gaussian are ellipses and what sets their axes.

Guidelines:

- Write 150 to 400 words.
- Start from the exponent of the density.
- Use the eigenvectors of the covariance matrix.
- Say what happens to the picture as the correlation approaches 1.

:::feynman{id=f1 prompt="Explain why the contours of a 2D Gaussian are ellipses and what sets their axes." key_points="The density depends on x only through the quadratic form (x - mu)^T Sigma^{-1} (x - mu), so contours are the sets where it is constant|In the coordinates of the eigenvectors of Sigma the quadratic form is a sum of squares divided by the eigenvalues, the equation of an ellipse|The axes point along the eigenvectors of the covariance matrix|The half-axes are proportional to the square roots of the eigenvalues, the standard deviations along those directions|As the correlation approaches 1 the small eigenvalue goes to 0 and the ellipse flattens toward a line"}
:::

## A written proof

:::feynman{id=proof1 prompt="Prove that every covariance matrix Sigma is positive semidefinite, and that Sigma is singular exactly when some nonzero combination a^T x of the coordinates has variance zero." key_points="Shows Var(a^T x) = a^T Sigma a by expanding the variance with linearity of expectation|Concludes a^T Sigma a >= 0 for every a, because a variance is nonnegative|If Sigma a = 0 for some nonzero a, then a^T Sigma a = 0, so a^T x has variance zero|Conversely, if a^T Sigma a = 0 for a positive semidefinite Sigma, writes a in the eigenvector basis to get a sum of lambda_i c_i^2 = 0, so every component with a positive eigenvalue vanishes and Sigma a = 0|Concludes that Sigma is singular exactly when a nonzero combination of the coordinates is constant"}
:::
