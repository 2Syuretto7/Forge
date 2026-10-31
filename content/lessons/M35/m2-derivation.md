# Derivation: power laws, nonlinear fitting and extrapolation

## 1. Power laws and scale invariance

A power law $f(x) = Ax^{-\alpha}$ is the only kind of function that looks the same at every scale: $f(cx)/f(x) = c^{-\alpha}$ does not depend on $x$. Taking logarithms, $\log f = \log A - \alpha\log x$, a straight line with slope $-\alpha$ on log-log axes, where each factor of 10 is one step. Loss curves of language models follow power laws in parameters, data and compute over many orders of magnitude, with one amendment: a floor $E$ that no amount of scale removes, the entropy of the text itself. The working model is

$$
L(x) = E + Ax^{-\alpha} .
$$

::::derivation{id=d1 title="A factor of ten"}
:::step
With $\alpha = 0.3$, every tenfold increase of $x$ multiplies the reducible loss $Ax^{-\alpha}$ by $10^{-0.3} \approx$ [[0.501|tol=0.002]]: it halves, at every scale.
:::
::::

## 2. Log-log regression and its biases

The cheapest fit regresses $\log y$ on $\log x$ by ordinary least squares (M25). It is the maximum-likelihood fit when the noise is multiplicative and lognormal, $y = Ax^{-\alpha}e^\varepsilon$. It has two biases. First, it fits the median, not the mean: if $\varepsilon \sim N(0, \sigma^2)$ then $\mathbb{E}y = Ax^{-\alpha}e^{\sigma^2/2}$, so exponentiating the fitted line underestimates averages; Duan's smearing factor, the mean of $e^{\text{residual}}$, corrects it. Second, and worse, it assumes there is no floor. With $E > 0$ the curve bends on log-log axes, but gently, so the line still fits with a high $R^2$ while its slope is wrong.

::::predict{id=p3 kind=choice answer=b}
Losses scatter around a power law with lognormal noise, $\sigma = 0.4$ in log space. You fit in log space and exponentiate. By how much does the prediction miss the average loss at a given $x$?

- Not at all: least squares is unbiased.
- About 8 percent too low.
- About 40 percent too low.
- About 8 percent too high.

:::reveal
About 8 percent too low: $e^{\sigma^2/2} = e^{0.08} \approx 1.083$. The log-space fit is unbiased for $\log y$, and $\log$ is concave, so the exponentiated fit is the median, below the mean. e03 measures it and corrects it.
:::
::::

::::derivation{id=d2 title="The lognormal factor"}
:::step
For $\sigma = 0.4$ the mean exceeds the median by the factor $e^{0.4^2/2} \approx$ [[1.083|tol=0.001]].
:::
::::

## 3. Gauss-Newton and Levenberg-Marquardt

$L(x; \theta)$ with $\theta = (E, A, \alpha)$ is linear in $E$ and $A$ but not in $\alpha$. Minimize the squared error $\lVert r(\theta)\rVert^2$, $r_i = y_i - L(x_i; \theta)$, by linearizing: $L(x; \theta + \delta) \approx L(x; \theta) + J\delta$ with the Jacobian $J_{ij} = \partial L(x_i)/\partial\theta_j$, whose columns are $1$, $x^{-\alpha}$ and $-Ax^{-\alpha}\ln x$. The best step for the linearized problem solves the normal equations

$$
J^\top J\,\delta = J^\top r ,
$$

the **Gauss-Newton** step: Newton's method on the squared error with the term involving second derivatives of the model dropped, which is small near a good fit. Far from it, the linearization is poor and Gauss-Newton can overshoot into regions where $x^{-\alpha}$ overflows. **Levenberg-Marquardt** adds damping,

$$
\big(J^\top J + \lambda\,\mathrm{diag}(J^\top J)\big)\,\delta = J^\top r ,
$$

and adapts $\lambda$: divide it by 3 after a step that lowers the error, multiply it by 3 and retry after one that does not. Small $\lambda$ recovers Gauss-Newton's fast convergence near the answer; large $\lambda$ gives short steps along a rescaled gradient (M29), which always make progress. The fit is badly conditioned when $\ln x$ varies little relative to its size, because the columns for $A$ and $\alpha$ become nearly proportional; measuring $x$ from a reference scale, $\ln(x/x_0)$, removes most of the problem.

::::derivation{id=d3 title="A column of the Jacobian"}
:::step
At $x = 100$ with $A = 2$ and $\alpha = 0.5$, the derivative of $L$ with respect to $\alpha$ is $-Ax^{-\alpha}\ln x = -2 \times 0.1 \times 4.605 \approx$ [[-0.921|tol=0.002]].
:::
::::

## 4. How sure is the fit?

Near the optimum the model is nearly linear in $\theta$, so the linear-regression formulas of M25 carry over with $J$ in place of the design matrix. With $s^2 = \lVert r\rVert^2/(n - p)$ for $n$ points and $p$ parameters,

$$
\widehat{\operatorname{Cov}}(\hat\theta) = s^2(J^\top J)^{-1} .
$$

The **residual bootstrap** checks this without the linear approximation: resample the residuals of the fitted curve, add them back to the fitted values, refit, and repeat. The spread of the refits estimates the uncertainty; their percentiles give intervals. Both assume independent errors of equal size, and both describe noise in the parameters given the model, not doubt about the model.

## 5. Prediction bands and extrapolation

A prediction $\hat L(x_0) = L(x_0; \hat\theta)$ has, by the delta method, standard error

$$
\operatorname{se}\big(\hat L(x_0)\big) \approx \sqrt{g^\top\widehat{\operatorname{Cov}}(\hat\theta)\,g}, \qquad g = \nabla_\theta L(x_0; \hat\theta) .
$$

Inside the data, errors in the parameters partly cancel. Outside, the component $-Ax_0^{-\alpha}\ln x_0$ lets an error in $\alpha$ act through a growing $\ln x_0$, until the shrinking $x_0^{-\alpha}$ wins and the band settles at the uncertainty of $E$. For a straight line in log space with $n$ points the exact prediction interval for a new observation is

$$
\hat v(u_0) \pm t_{n-2}\,s\sqrt{1 + \frac1n + \frac{(u_0 - \bar u)^2}{\sum_i(u_i - \bar u)^2}} ,
$$

where Student's quantile $t_{n-2}$ accounts for estimating $s$ from $n - 2$ degrees of freedom: $3.18$ for five points, against $1.96$ for many.

::::derivation{id=d4 title="Five points, a hundred times out"}
:::step
Five runs evenly spaced in $u = \ln x$ over $[0, \ln 100]$ and a target at $x_0 = 10^4$: the factor under the square root is $1 + \frac15 + \frac{6.91^2}{13.26} \approx 4.8$, so the standard error is inflated by about [[2.19|tol=0.01]].
:::
::::

## 6. Fitting L(N, D) and the compute-optimal frontier

For language models the loss depends on parameters $N$ and tokens $D$ separately:

$$
L(N, D) = E + \frac A{N^\alpha} + \frac B{D^\beta} ,
$$

fitted by Levenberg-Marquardt in the centred parametrization $L = E + e^{a - \alpha\ln(N/N_0)} + e^{b - \beta\ln(D/D_0)}$. Training costs about $C = 6ND$ flops (L11). At fixed $C$, substitute $D = C/(6N)$ and set the derivative in $N$ to zero: $\alpha AN^{-\alpha} = \beta B(C/6N)^{-\beta}$, so

$$
N_{\text{opt}} = \Big(\frac{\alpha A}{\beta B}\Big)^{\frac1{\alpha + \beta}}\Big(\frac C6\Big)^{\frac\beta{\alpha + \beta}}, \qquad D_{\text{opt}} \propto C^{\frac\alpha{\alpha + \beta}} .
$$

:::edge{to=L11 text="your fitting machinery produces the scaling-law fit."}
:::

::::derivation{id=d5 title="Splitting compute"}
:::step
With Chinchilla's $\alpha = 0.34$ and $\beta = 0.28$, the optimal parameter count grows like $C^{\beta/(\alpha + \beta)}$ with exponent [[0.452|tol=0.002]]: parameters and data should grow almost equally.
:::
::::

## 7. When the line lies

Two failures no error bar reports. **A missing floor**: a straight line through data that bend toward $E$ has a slope too shallow inside the data and a forecast that falls through the floor beyond it. **A changing law**: if the exponent changes beyond the data, because a new regime begins, data run out, or the architecture saturates, the fit is excellent, the bands are narrow, and the truth lies outside them. The bands quantify noise given the model; only runs closer to the target scale test the model. The practical rules: fit the floor, extrapolate as short a distance as the decision allows, and check with one run at an intermediate scale before committing to the largest.

:::edge{to=M38 text="extrapolation from small experiments to frontier runs."}
:::

## Summary

| Idea | Statement | Use |
| --- | --- | --- |
| Power law | $f(cx)/f(x) = c^{-\alpha}$; straight on log-log axes | scale-free trends |
| Log-space fit | fits the median; mean is $e^{\sigma^2/2}$ higher | quick fits, with smearing |
| Gauss-Newton | $J^\top J\delta = J^\top r$ | fast near the answer |
| Levenberg-Marquardt | $(J^\top J + \lambda\,\mathrm{diag}(J^\top J))\delta = J^\top r$, adaptive $\lambda$ | robust nonlinear fits |
| Uncertainty | $s^2(J^\top J)^{-1}$; residual bootstrap | standard errors, intervals |
| Prediction band | $\sqrt{g^\top\mathrm{Cov}\,g}$; Student's $t$ for few points | honest forecasts |
| Frontier | $N_{\text{opt}} \propto C^{\beta/(\alpha + \beta)}$ | splitting compute |
