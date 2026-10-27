# Puzzle: zero training error, twice

You fit polynomials to 20 noisy points of a smooth curve. A degree-19 polynomial passes through every point: zero training error, and wild oscillations between the points. Its test error is enormous.

Now you fit a much larger model, with 80 parameters, to the same 20 points. It also passes through every point with zero training error.

::::predict{id=p1 kind=choice answer=c}
What do you expect of the 80-parameter model's test error compared with the 20-parameter one that interpolates?

- Much worse: four times the parameters, four times the overfitting.
- The same: both interpolate, so both overfit equally.
- It can be much better, if among all the interpolating solutions you pick the one with the smallest norm.
- Exactly zero, because it has more parameters than data points.

:::reveal
When there are more parameters than data points, infinitely many parameter vectors fit the data exactly. The one gradient descent from zero finds, the minimum-norm solution, spreads the fit over many directions and does not need any single direction to be huge. Near the threshold (parameters equal to data points) there is exactly one interpolant and it must use huge coefficients to hit every noisy point. So test error rises toward the threshold, peaks there, and falls again beyond it: **double descent**.
:::
::::

The classical picture says test error is U-shaped in model capacity: too simple underfits, too complex overfits, pick the middle. Modern neural networks are trained far past the point where they could memorize their training set, and they generalize. The widget below shows both pictures in one curve. The dashed vertical line marks the point where the number of features equals the number of training points.

:::widget{name=BiasVarianceCurve n=20 noise=0.3}
:::

::::predict{id=p2 kind=sketch answer="0.36,0.35,0.28,0.61,1,0.24,0" tol=0.2 xlabel="number of features: 2, 5, 10, 17, 20, 30, 80" ylabel="log test error (scaled)"}
Sketch the logarithm of the widget's test error (before touching the sliders) at 2, 5, 10, 17, 20, 30 and 80 features, scaled so the largest value is 1 and the smallest 0.

:::reveal
The test errors are about $0.92, 0.90, 0.64, 3.2, 21, 0.53, 0.16$: a shallow U on the left (falling to $p = 10$, then rising as $p$ approaches $n$), a spike at $p = n = 20$ that is more than twenty times the bottom of the U, then a second descent that ends well below the bottom of the U. On a linear axis the spike would dwarf everything else, which is why double-descent plots use a log scale.
:::
::::

## Questions to carry into the derivation

1. How exactly does test error split into parts we can reason about?
2. Why is the error worst at the interpolation threshold?
3. What does gradient descent choose when many solutions fit perfectly?
4. How do we measure test error without fooling ourselves?
