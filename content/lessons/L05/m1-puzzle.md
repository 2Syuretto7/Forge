# Puzzle: the same data, two losses, two answers

You have house sizes and prices, and you want to predict price from size. One colleague minimizes squared error. Another minimizes absolute error. A third fits a line by eye. A fourth points out that a few houses are mansions whose prices are wildly off the trend.

::::predict{id=p1 kind=choice answer=b}
Which loss should you use, and why?

- Squared error, because it is the standard.
- It depends on what you believe about the noise: squared error is maximum likelihood for Gaussian noise, absolute error for Laplace (heavy-tailed) noise.
- Absolute error, because it is more robust and therefore always better.
- It makes no difference; all reasonable losses give the same line.

:::reveal
A loss is a statement about noise. If residuals are Gaussian, minimizing squared error is maximum likelihood and gives the most efficient estimate. If the noise has heavy tails (a few mansions), squared error lets those points drag the line, and absolute error (maximum likelihood under Laplace noise) is the better model. The losses give different lines whenever the data contain outliers.
:::
::::

Classification raises the same question in sharper form. You want to predict whether an email is spam from a few word counts. You could regress the label (0 or 1) with squared error, but predictions would wander outside $[0, 1]$ and outliers far from the boundary would pull it around. The right model says each label is a coin flip whose probability depends on the features, and fits that probability by maximum likelihood. That is **logistic regression**.

::::predict{id=p2 kind=choice answer=c}
You train logistic regression by gradient descent on two classes that a straight line separates perfectly, with no regularization. What happens to the weights as training continues?

- They converge to the maximum-margin separator.
- They converge to some finite separating vector and stop.
- Their norm keeps growing without bound.
- They oscillate.

:::reveal
Any separating direction can be scaled up to push every predicted probability closer to the right label, so the loss keeps decreasing and has no finite minimizer. The norm grows forever (logarithmically in the number of steps). Remarkably, the direction converges to the maximum-margin separator, but the weights themselves do not converge. An L2 penalty restores a finite optimum. Try it in the widget: turn on "Separable classes" and watch the weight norm.
:::
::::

:::widget{name=DecisionBoundary separable=true lr=1}
:::

## Questions to carry into the derivation

1. Which noise model turns maximum likelihood into least squares, and which into logistic regression?
2. What are the gradients, and why do they have the same form for both models?
3. What does L2 regularization mean, and what does it fix?
4. How do you know whether predicted probabilities can be trusted?
