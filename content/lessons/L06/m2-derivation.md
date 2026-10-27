# Derivation: what test error is made of

This movement defines the quantity we care about (risk on new data), decomposes its expected value into noise, bias and variance, and uses the decomposition to explain both the classical U-shaped curve and double descent. It ends with the rules for estimating risk honestly: held-out sets, cross-validation, and the two ways to leak.

## 1. Risk and its estimates

Data come from an unknown distribution: inputs $x$ and targets $y = f(x) + \epsilon$ with noise $\mathbb{E}\epsilon = 0$, $\operatorname{Var}\epsilon = \sigma^2$. A learning algorithm takes a training set $\mathcal D$ of $n$ points and returns a predictor $\hat f_{\mathcal D}$. Its **risk** is the expected loss on a fresh point, $R(\hat f) = \mathbb{E}_{x,y}\big[(y - \hat f(x))^2\big]$. Its **training error** is the average loss on $\mathcal D$ itself, which is optimistic: the predictor was chosen to make exactly those losses small.

A **test set** drawn independently of $\mathcal D$ gives an unbiased estimate of the risk, but only as long as nothing about the predictor was chosen by looking at it. The moment you pick a model, a hyperparameter or a feature because it scored well on the test set, its score becomes a training error in disguise (Movement 5).

## 2. The bias-variance decomposition

Fix an input $x$ and consider the randomness of the training set. Write $\bar f(x) = \mathbb{E}_{\mathcal D}[\hat f_{\mathcal D}(x)]$ for the average prediction over training sets.

::::derivation{id=d1 title="Splitting the expected error at one point"}
:::step
Write $y - \hat f = (y - f) + (f - \bar f) + (\bar f - \hat f)$, dropping the argument $x$. The three pieces are the noise $\epsilon$, a fixed number (the **bias**), and a zero-mean random variable (the **fluctuation**). Square and take expectations over the noise and the training set. The noise is independent of the training set and has mean zero, so every cross term involving it vanishes. The term $2(f - \bar f)\,\mathbb{E}[\bar f - \hat f]$ vanishes because $\mathbb{E}[\hat f] =$ [[word:fbar/f bar/the average prediction/average prediction]].
:::
:::step
What remains is $\mathbb{E}[(y - \hat f)^2] = \sigma^2 + (f - \bar f)^2 + \mathbb{E}[(\hat f - \bar f)^2]$: **noise + bias squared + variance**. If the noise variance is $0.09$, the squared bias $0.01$ and the variance $0.05$, the expected error at that point is [[0.15]].
:::
:::step
Averaging over $x$ gives the same split for the risk. The noise term is the floor no model can beat. In a polynomial fit, raising the degree lowers the bias and raises the variance. If a degree-1 model has bias squared $0.4$ and variance $0.01$ while a degree-15 model has bias squared $0.001$ and variance $0.6$, with noise $0.09$, the better of the two has expected error [[0.5]].
:::
::::

:::edge{from=L02 text="bias and variance of estimators"}
:::

The decomposition explains the classical U. Simple models are wrong in the same way on every training set (high bias, low variance). Flexible models follow the noise of whichever training set they see (low bias, high variance). Somewhere in between the sum is smallest.

## 3. Regularization moves along the tradeoff

Ridge regression (L05) shrinks coefficients toward zero. That adds bias (the shrunk fit is systematically too small) and removes variance (the fit moves less from one training set to the next). A useful way to measure a ridge model's capacity is its **effective degrees of freedom**,

$$
\mathrm{df}(\lambda) = \operatorname{tr}\big(X(X^\top X + \lambda I)^{-1}X^\top\big) = \sum_j \frac{s_j^2}{s_j^2 + \lambda},
$$

where $s_j$ are the singular values of $X$. At $\lambda = 0$ it counts the parameters; as $\lambda$ grows it slides continuously to zero. Each direction is kept in proportion to how strongly the data support it, the same singular-value story as L01.

## 4. More parameters than data: interpolation and the minimum norm

With $p > n$ features (and $X$ of full row rank) the equations $Xw = y$ have infinitely many solutions. The **minimum-norm interpolant** is

$$
\hat w = X^\top (X X^\top)^{-1} y ,
$$

the solution with no component in the null space of $X$. It is also what you get from ridge as $\lambda \to 0$, and from gradient descent started at zero.

::::derivation{id=d2 title="Gradient descent from zero picks the minimum norm"}
:::step
The gradient of $\|Xw - y\|^2$ is $2X^\top(Xw - y)$, a combination of the rows of $X$. Starting from $w_0 = 0$, every iterate is a sum of such vectors, so it always lies in the [[word:row space/row space of X/span of the rows]].
:::
:::step
The interpolating solutions are $\hat w + v$ for $v$ in the null space, and the null space is orthogonal to the row space. The only interpolant inside the row space is the one with $v =$ [[0]], which is $\hat w$, so gradient descent converges to the minimum-norm solution.
:::
::::

This **implicit regularization** is one reason overparameterized models generalize: the training algorithm, not just the model class, decides which of the many perfect fits you get.

## 5. Why the peak sits at p = n

Isolate the variance by taking a target with no signal, $y = \epsilon$, and inputs with independent standard Gaussian features. Then the fitted weights are pure noise amplification, and for isotropic inputs the excess test error equals $\mathbb{E}\|\hat w\|^2$. Random-matrix results for Gaussian designs give it exactly:

$$
\mathbb{E}\|\hat w\|^2 = \begin{cases} \sigma^2 \dfrac{p}{n - p - 1}, & p < n - 1 \text{ (least squares)},\\[2mm] \sigma^2 \dfrac{n}{p - n - 1}, & p > n + 1 \text{ (minimum norm)}. \end{cases}
$$

::::derivation{id=d3 title="Reading the variance formula"}
:::step
With $n = 20$ points and noise $\sigma^2 = 1$, a model with $p = 10$ features has variance $10/(20 - 10 - 1) \approx$ [[1.111]].
:::
:::step
At $p = 18$ it has $18/1 = 18$. Beyond the threshold, at $p = 60$, it is $20/(60 - 20 - 1) \approx$ [[0.5128]].
:::
:::step
Both expressions blow up as $p \to n$. The reason is conditioning (L01): the variance is $\sigma^2\operatorname{tr}\big((X^\top X)^{-1}\big)$ or $\sigma^2\operatorname{tr}\big((XX^\top)^{-1}\big)$, a sum of $1/s_j^2$, and the smallest singular value of an $n \times p$ Gaussian matrix is about $|\sqrt{p} - \sqrt{n}|$. At $p = n = 400$ that approximation gives [[0]], and the noise is divided by it.
:::
::::

With signal present, the bias falls as $p$ grows (more features capture more of the target), and the variance follows the curve above. The sum is the double-descent curve of the widget: a U on the left, a spike at $p = n$, and a second descent on the right that can end below the bottom of the U when the signal is spread over many directions. Ridge regularization caps $1/s_j^2$ at $1/\lambda$ and removes the spike.

:::widget{name=BiasVarianceCurve n=20 noise=0.3 loglambda=-9}
:::

Move the ridge slider: by $\lambda \approx 10^{-1}$ the peak is gone and the curve is monotone. Optimal regularization never has a double-descent peak; the peak is the signature of fitting noise exactly with too few directions to spread it over.

## 6. Estimating risk honestly

**Hold-out.** Split once into training and test. Simple and unbiased if the test set is touched once at the end; noisy if the test set is small (L02's standard error applies: an accuracy measured on 100 examples is uncertain by about $\pm 5$ points).

**k-fold cross-validation.** Split the data into $k$ folds; train on $k - 1$, evaluate on the held-out fold, rotate, and average. Every point is used for evaluation exactly once. Use it to choose hyperparameters, then refit on all training data and report a separate test score.

::::derivation{id=d4 title="Cross-validation bookkeeping"}
:::step
With $n = 200$ training points and $k = 5$ folds, each model is trained on [[160]] points.
:::
:::step
Evaluating 8 candidate degrees with 5-fold CV requires [[40]] model fits, plus one final refit.
:::
:::step
To estimate the risk of the whole procedure (selection included), wrap it in an outer loop: **nested** cross-validation. With 5 outer folds, each running the 40-fit inner search plus a refit, that is $5 \times 41 =$ [[205]] fits.
:::
::::

**The two classic leaks.** Any step that looks at labels must happen inside the cross-validation loop: feature selection, standardization statistics, target encoding, choosing a threshold. Doing it on the full data first makes the cross-validated score optimistic, sometimes absurdly so. And any score used to make a choice is no longer an unbiased estimate: the maximum of many noisy test scores overstates the winner. Movement 5 builds both failures from pure noise.

:::edge{to=L16 text="Benchmark contamination: test data that leaked into a pretraining corpus inflate scores the same way."}
:::

:::edge{to=L15 text="Scaling laws model test loss as an irreducible floor plus terms that shrink with data and parameters."}
:::

## Summary

| Idea | Formula or rule | Consequence |
| --- | --- | --- |
| Decomposition | noise $+$ bias$^2$ $+$ variance | the classical U |
| Ridge capacity | $\mathrm{df}(\lambda) = \sum s_j^2/(s_j^2 + \lambda)$ | regularization as a dial |
| Minimum norm | $X^\top(XX^\top)^{-1}y$, reached by GD from zero | implicit regularization |
| Variance at the threshold | $\sigma^2 p/(n-p-1)$, $\sigma^2 n/(p-n-1)$ | the double-descent spike |
| Honest evaluation | everything that sees labels goes inside the CV loop | no leaks |
