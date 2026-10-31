# Prediction bands and how they grow

A prediction $\hat L(x_0) = L(x_0; \hat\theta)$ inherits the uncertainty of $\hat\theta$. To first order, with $g = \nabla_\theta L(x_0; \hat\theta)$, the **delta method** gives (Section 5)

$$
\operatorname{se}\big(\hat L(x_0)\big) \approx \sqrt{g^\top\,\widehat{\operatorname{Cov}}(\hat\theta)\,g} .
$$

Inside the data the parameters' errors partly cancel; beyond it the term $Ax_0^{-\alpha}\ln x_0$ in $g$ lets an error in $\alpha$ grow with $\ln x_0$ until the shrinking factor $x_0^{-\alpha}$ wins.

- `prediction(theta, x0)` and `grad_prediction(theta, x0)`: the model and its gradient in $\theta$.
- `prediction_se(theta, cov, x0)`.
- `band(theta, cov, xs, z=1.96)`: lower and upper arrays.

The tests run a **gradient check** and find the band at 10 and 100 times the largest data point wider than anywhere inside the data.

## Hints

1. The gradient in $\theta$ is a row of e04's Jacobian, evaluated at $x_0$.
2. `cov` is $3 \times 3$; `g @ cov @ g` is the variance.
3. Far enough out, $L \to E$ and the band's width approaches that of $E$ alone: extrapolation is limited by how well the floor is known.
