# Puzzle: height and weight

Height and weight in an adult population are roughly jointly Gaussian with correlation about $0.5$.

::::predict{id=p1 kind=numeric answer=13 tol=4}
You learn someone's height exactly. By what percentage does the standard deviation of your guess of their weight shrink?

:::reveal
About 13 percent. The conditional standard deviation is $\sigma_w\sqrt{1 - \rho^2} = \sigma_w\sqrt{0.75} \approx 0.87\,\sigma_w$. A correlation of $0.5$ sounds strong, but it removes only a quarter of the variance, $\rho^2$, and an eighth of the standard deviation. Height tells you where to center the guess, along the regression line, much more than it narrows it.
:::
::::

::::predict{id=p2 kind=choice answer=b}
Two variables each have standard deviation 1 and correlation $0.9$. What does the cloud of samples look like?

- A circle: each variable alone has the same spread.
- An ellipse along the 45-degree line, about 4 times longer than wide.
- An ellipse along the 45-degree line, about twice as long as wide.
- Points on a straight line.

:::reveal
An ellipse along the diagonal with axis ratio $\sqrt{1.9/0.1} \approx 4.4$. The covariance matrix $\begin{pmatrix} 1 & 0.9 \\ 0.9 & 1\end{pmatrix}$ has eigenvectors $(1, 1)$ and $(1, -1)$ with eigenvalues $1.9$ and $0.1$, and the ellipse's half-axes are the square roots of the eigenvalues. Only at correlation 1 does the cloud collapse to a line.
:::
::::

Move the correlation and the observed $x$. The ellipses mark 1, 2 and 3 standard deviations; the vertical bar is the conditional range of $y$ given $x$. Its center slides along the regression line as $x$ moves, but its length does not change.

:::widget{name=GaussianEllipse sx=1 sy=1 rho=0.5 x0=1.5}
:::

## Questions to carry into the derivation

1. How do you get the distribution of one variable from the joint distribution of several?
2. What object holds all the variances and covariances, and what property must it have?
3. Why are the contours of a Gaussian ellipses, and what sets their axes?
4. How does observing some coordinates change the distribution of the others?
