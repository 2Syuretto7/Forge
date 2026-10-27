# Break it: unscaled features and separable data

## Unscaled features

Section 5 predicted that badly scaled features make gradient descent crawl. The next exercise measures it: same data, same model, with and without standardization.

:::exercise{ref=e10}
:::

## Separable data

When a hyperplane separates the training classes perfectly, unregularized logistic regression has no minimizer. The weights grow forever, predicted probabilities on the training data race toward exactly 0 and 1, and the model becomes arbitrarily overconfident on test points near the boundary.

::::predict{id=p5 kind=sketch answer="0,0.33,0.5,0.6,0.67,0.72,0.77" xlabel="training step (log scale, 1 to 1e6)" ylabel="weight norm (scaled)"}
On separable data, sketch the weight norm of gradient descent against the number of steps on a log scale, at $10^0, 10^1, \dots, 10^6$ steps.

:::reveal
After an initial transient the norm grows like $\log t$: a straight line on a log-scale axis, rising forever with no plateau. With an L2 penalty the curve instead flattens at a finite value. The exact slope depends on the margin; only the shape matters here.
:::
::::

:::exercise{ref=e11}
:::

## What to take away

- Always standardize features for gradient-based training, with statistics from the training split only.
- Always regularize logistic and softmax regression a little; an L2 penalty is cheap insurance against separable data and duplicated features.
- Watch the weight norm: steady growth with falling training loss and flat validation loss is the signature of overconfidence.
