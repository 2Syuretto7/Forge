# Explain it plainly: logistic regression

Explain to someone who knows what a straight-line fit is how logistic regression turns features into a probability, why its loss is what it is, and how training changes the weights.

- Write 150 to 400 words.
- Use a concrete example, such as spam filtering with two word counts.
- Explain why the loss is the log-likelihood of coin flips and why that is better than squared error on 0/1 labels.
- Say what the gradient update does in plain terms.

:::feynman{id=f1 prompt="Explain how logistic regression turns features into a probability, why its loss is the negative log-likelihood of Bernoulli outcomes, and what one step of gradient descent does to the weights." key_points="A weighted sum of features gives a score that the sigmoid squashes into a probability between 0 and 1|Each label is treated as a coin flip with that probability, and the loss is minus the log of the probability given to the actual label|The gradient for each example is the feature vector times the prediction error, so wrong confident predictions move the weights most|The decision boundary is where the score is zero, a straight line or hyperplane|Without regularization the weights grow forever on perfectly separable data"}
:::
