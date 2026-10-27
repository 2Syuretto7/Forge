# Explain it plainly: double descent

Explain to someone who learned "more parameters means more overfitting" why a model with many more parameters than training examples can generalize better than one with exactly as many.

- Write 150 to 400 words.
- Use a concrete example with numbers of points and parameters.
- Explain what is special about the point where parameters equal data points.
- Say what the training procedure contributes.

:::feynman{id=f1 prompt="Explain the double-descent curve: why test error rises as the number of parameters approaches the number of training points, peaks there, and falls again with even more parameters." key_points="Test error is noise plus squared bias plus variance, and the classical U comes from bias falling while variance rises|At the interpolation threshold there is exactly one perfect fit and it needs huge coefficients to pass through every noisy point|Huge coefficients come from a nearly singular design, with a smallest singular value close to zero, which amplifies noise|With more parameters than points, many perfect fits exist and gradient descent from zero picks the smallest one, which spreads the fit out|Regularization such as ridge removes the peak"}
:::
