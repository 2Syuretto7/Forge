# Puzzle: a straight line on the wrong axes

A training run's loss, plotted against the amount of compute on ordinary axes, is a curve that drops steeply and then flattens. Plotted with **both** axes logarithmic (each step along an axis multiplies by ten instead of adding a fixed amount), the same points fall on a straight line.

::::predict{id=p1 kind=choice answer=c}
A straight line on log-log axes means what kind of law?

- A straight line: loss falls by the same amount for each unit of compute.
- An exponential: loss falls by the same factor for each unit of compute.
- A power law: loss falls by the same factor each time compute is multiplied by the same factor.
- No law at all; log axes distort everything.

:::reveal
A power law, $L = C\,x^{-p}$. Taking logarithms, $\log L = \log C - p \log x$: a straight line in $\log x$ with slope $-p$. Multiplying compute by 10 moves one step right on the log axis and lowers $\log L$ by a fixed amount, which is multiplying $L$ by the fixed factor $10^{-p}$. Scaling laws for language models (L11, M35) are exactly such lines.
:::
::::

::::predict{id=p2 kind=numeric answer=0.15 tol=0.02}
On log-log axes, the loss halves (from 4 to 2) while compute grows by a factor of 100. If the law is $L = C x^{-p}$, what is $p$?

:::reveal
$\frac{L_2}{L_1} = 100^{-p} = \frac{1}{2}$, so $p = \frac{\log 2}{\log 100} = \frac{0.301}{2} \approx 0.15$. Halving the loss costs a hundred times the compute: power laws with small exponents are why each step of progress costs so much more than the last.
:::
::::

Try the widget: pick a dataset, then switch each axis between linear and logarithmic until the points line up. Which axes straighten which law?

:::widget{name=LogScaler data=power}
:::

## Questions to carry into the derivation

1. What could $2^{0.5}$ or $2^\pi$ possibly mean?
2. Where does the number $e \approx 2.718$ come from?
3. Why does the logarithm turn multiplication into addition?
4. How do you compute $e^{1000} / (e^{1000} + e^{999})$ when $e^{1000}$ is too large for any computer?
