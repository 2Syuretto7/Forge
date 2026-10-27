# Derivation: regression from noise models

Every model in this lesson follows the same recipe: write down a probabilistic model of how labels arise from features, take the negative log-likelihood as the loss, compute its gradient, and minimize. Linear regression, logistic regression and softmax regression are three instances. You will also see where L2 regularization comes from and how to measure whether predicted probabilities mean what they say.

## 1. Linear regression is maximum likelihood under Gaussian noise

Data: feature rows $x_i \in \mathbb{R}^d$ stacked in $X \in \mathbb{R}^{n \times d}$, targets $y \in \mathbb{R}^n$. Model: $y_i = w^\top x_i + \epsilon_i$ with independent $\epsilon_i \sim \mathcal N(0, \sigma^2)$. (Absorb an intercept by appending a constant feature 1.)

::::derivation{id=d1 title="From the Gaussian likelihood to least squares"}
:::step
The log-likelihood is $\sum_i \log\mathcal N(y_i; w^\top x_i, \sigma^2) = -\tfrac{n}{2}\log(2\pi\sigma^2) - \dfrac{1}{2\sigma^2}\sum_i (y_i - w^\top x_i)^2$. For fixed $\sigma$, maximizing it over $w$ is the same as minimizing $\sum_i (y_i - w^\top x_i)^2$. For a single point with residual $r = y - w^\top x$, the term being minimized is [[r^2]].
:::
:::step
The gradient of $L(w) = \tfrac{1}{n}\|Xw - y\|^2$ is $\tfrac{2}{n}X^\top(Xw - y)$. Setting it to zero gives the normal equations of L01. For a one-feature model with no intercept, $\hat w = \sum x_i y_i / \sum x_i^2$. With data $(1, 2), (2, 3)$ that is $(2 + 6)/(1 + 4) =$ [[1.6]].
:::
:::step
Maximizing over $\sigma^2$ as in L02 gives $\hat\sigma^2 = \tfrac{1}{n}\sum_i (y_i - \hat w^\top x_i)^2$, the mean squared residual. With residuals $0.2$ and $-0.2$, $\hat\sigma^2 =$ [[0.04]].
:::
::::

:::edge{from=L01 text="least squares and the normal equations"}
:::

## 2. Ridge regression is MAP with a Gaussian prior

Put a prior $w \sim \mathcal N(0, \tau^2 I)$ on the weights. The log-posterior is the log-likelihood plus $-\|w\|^2/(2\tau^2)$, so the MAP estimate minimizes

$$
\sum_i (y_i - w^\top x_i)^2 + \lambda \|w\|^2, \qquad \lambda = \sigma^2/\tau^2 .
$$

Setting the gradient $2X^\top(Xw - y) + 2\lambda w$ to zero gives the **ridge** solution

$$
\hat w_\lambda = (X^\top X + \lambda I)^{-1} X^\top y .
$$

Adding $\lambda I$ lifts every eigenvalue of $X^\top X$ by $\lambda$, so it also cures the ill-conditioning of L01: the condition number becomes $(\sigma_{\max}^2 + \lambda)/(\sigma_{\min}^2 + \lambda)$.

::::derivation{id=d2 title="Shrinkage in one dimension"}
:::step
With one feature, ridge gives $\hat w_\lambda = \dfrac{\sum x_i y_i}{\sum x_i^2 + \lambda}$. If $\sum x_i y_i = 8$ and $\sum x_i^2 = 5$, then $\lambda = 5$ gives $\hat w =$ [[0.8]]: half the least-squares value.
:::
:::step
A strong prior (small $\tau^2$) means a large $\lambda$. As $\lambda \to \infty$, $\hat w_\lambda \to$ [[0]].
:::
:::step
If the noise variance is $\sigma^2 = 0.25$ and the prior variance is $\tau^2 = 0.05$, then $\lambda = \sigma^2/\tau^2 =$ [[5]].
:::
::::

:::edge{from=L02 text="maximum likelihood and Gaussian priors"}
:::

## 3. Logistic regression is maximum likelihood for coin flips

For labels $y_i \in \{0, 1\}$, model each label as a Bernoulli variable whose probability is a squashed linear score: $P(y_i = 1 \mid x_i) = \sigma(w^\top x_i + b)$ with the **sigmoid** $\sigma(a) = 1/(1 + e^{-a})$. The decision boundary $\{x : w^\top x + b = 0\}$ is a hyperplane, and the score $a = w^\top x + b$ is the **log-odds**: $\log\dfrac{P(y=1)}{P(y=0)} = a$.

The negative log-likelihood per example is the binary cross-entropy of L04,

$$
\ell_i = -y_i \log\sigma(a_i) - (1 - y_i)\log\big(1 - \sigma(a_i)\big).
$$

::::derivation{id=d3 title="The logistic gradient"}
:::step
Use $\sigma'(a) = \sigma(a)(1 - \sigma(a))$. The derivative of $-\log\sigma(a)$ is $-(1 - \sigma(a))$, and the derivative of $-\log(1 - \sigma(a))$ is $\sigma(a)$. So $\partial\ell/\partial a = -y(1 - \sigma(a)) + (1-y)\sigma(a)$, which simplifies to [[s - y]], writing s for $\sigma(a)$.
:::
:::step
By the chain rule, $\partial\ell_i/\partial w = (\sigma(a_i) - y_i)\, x_i$. Averaging over the data, $\nabla_w L = \tfrac{1}{n}X^\top(\sigma(Xw + b) - y)$. For one example with $x = 2$, $y = 1$ and $\sigma(a) = 0.7$, the gradient on $w$ is [[-0.6]].
:::
:::step
Compare with linear regression, whose gradient is $\tfrac{2}{n}X^\top(Xw - y)$: both are "features times prediction error". This shared form is a property of **generalized linear models** with their canonical link. The Hessian of the logistic loss is $\tfrac1n X^\top S X$ with $S = \operatorname{diag}(\sigma_i(1-\sigma_i))$, which is positive semidefinite, so the loss is convex and has no spurious local minima. For a single example at $\sigma = 0.5$, the weight $\sigma(1-\sigma)$ equals [[0.25]].
:::
::::

There is no closed form for the minimizer. Gradient descent works; Newton's method, which uses the Hessian, converges in a handful of iterations (exercise 12).

## 4. Softmax regression for many classes

For $K$ classes, give each class a weight vector $w_k$ and form logits $z_k = w_k^\top x + b_k$, then probabilities $p = \operatorname{softmax}(z)$. The loss is the categorical cross-entropy $-\log p_y$, and by L04 its gradient with respect to the logits is $p - e_y$. With $W \in \mathbb{R}^{d \times K}$, logits $Z = XW + \mathbf 1 b^\top$, probabilities $P$ and one-hot targets $Y$:

$$
\nabla_W L = \tfrac{1}{n} X^\top (P - Y), \qquad \nabla_b L = \tfrac1n \mathbf{1}^\top (P - Y).
$$

Logistic regression is the $K = 2$ case with one logit fixed at zero.

:::edge{to=L13 text="Attention weights are a softmax over similarity scores, exactly this function applied to dot products."}
:::

## 5. Optimization in practice: why features must be standardized

Gradient descent on a quadratic converges at a rate set by the condition number of the Hessian (L01, and in full detail L09). For linear regression the Hessian is $\tfrac{2}{n}X^\top X$. If one feature is measured in meters and another in millimeters, their scales differ by $10^3$ and the condition number by about $10^6$: the learning rate must be small enough for the steep direction, and the shallow direction then barely moves.

**Standardization** rescales each feature to mean 0 and standard deviation 1 using statistics computed on the **training set only**. It does not change what linear models can represent, only how fast gradient descent finds it. Computing the statistics on all data, including test data, leaks information about the test set into training; L06 makes that failure concrete.

::::derivation{id=d4 title="Condition number of two unscaled features"}
:::step
Two uncorrelated, zero-mean features with standard deviations $1$ and $1000$ give $\tfrac1n X^\top X \approx \operatorname{diag}(1, 10^6)$. Its condition number is [[1e6]].
:::
:::step
The largest stable learning rate for gradient descent on $L(w) = \tfrac1n\|Xw - y\|^2$ is about $2/\lambda_{\max}$ where $\lambda_{\max} = 2 \times 10^6$ is the top Hessian eigenvalue. That is $10^{-6}$. The error along the shallow direction then shrinks by a factor $1 - \eta \cdot 2 \approx 1 - 2 \times 10^{-6}$ per step, so reducing it by $e^{-1}$ takes about [[500000|tol=5000]] steps.
:::
::::

## 6. Evaluating a probabilistic classifier

**Accuracy** counts correct argmax predictions. **Log loss** (mean cross-entropy on held-out data) also rewards being confident when right and punishes being confident when wrong; it is the quantity training minimizes. A model can have good accuracy and terrible log loss if it is overconfident.

**Calibration** asks whether predicted probabilities match frequencies: among examples where the model says "70 percent", about 70 percent should be correct. A **reliability diagram** bins predictions by confidence and plots the average confidence against the observed accuracy in each bin; a calibrated model lies on the diagonal. The **expected calibration error** summarizes it:

$$
\mathrm{ECE} = \sum_{b} \frac{n_b}{n}\,\big|\,\text{acc}(b) - \text{conf}(b)\,\big|.
$$

::::derivation{id=d5 title="Reading a calibration bin"}
:::step
A bin holds 50 predictions with average confidence $0.85$, of which 35 are correct. Its accuracy is $35/50 =$ [[0.7]].
:::
:::step
The model is overconfident in this bin by $0.85 - 0.7 =$ [[0.15]]. If the bin holds a fifth of the data, its contribution to the ECE is $0.2 \times 0.15 = 0.03$.
:::
::::

Maximum likelihood training tends to produce well-calibrated linear models when the model is right about the data. Large neural networks trained for many epochs are often overconfident, which is why calibration returns in L23's evaluation lesson.

## Summary

| Model | Noise / likelihood | Loss | Gradient on weights |
| --- | --- | --- | --- |
| Linear regression | Gaussian | squared error | $\tfrac2n X^\top(Xw - y)$ |
| Ridge | Gaussian + Gaussian prior | squared error $+ \lambda\|w\|^2$ | $\tfrac2n X^\top(Xw - y) + \tfrac{2\lambda}{n} w$ |
| Logistic regression | Bernoulli | binary cross-entropy | $\tfrac1n X^\top(\sigma(Xw) - y)$ |
| Softmax regression | categorical | cross-entropy | $\tfrac1n X^\top(P - Y)$ |
