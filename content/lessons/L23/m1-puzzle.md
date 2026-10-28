# Puzzle: is the new model better?

A new model scores 71.0% on a 500-item benchmark; the old one scored 69.5%. The release notes call it an improvement.

::::predict{id=p1 kind=choice answer=b}
What does the 1.5-point gap show?

- That the new model is better: 1.5 points on 500 items is 7 more correct answers.
- Little by itself: each score has a standard error of about 2 points, so the gap is within noise unless a paired, item-by-item comparison shows the models rarely disagree.
- That the old model is better, since benchmark gains usually come from contamination.
- Nothing at all: accuracy cannot be compared across models.

:::reveal
Each accuracy has standard error $\sqrt{0.7 \cdot 0.3 / 500} \approx 0.0205$; for two independent scores the difference has standard error about 0.029, so 1.5 points is half a standard error. Because both models face the same items, a paired comparison removes the variation they share and can be much sharper (exercise 2); the same item-level data also exposes contamination, if the new model does suspiciously well on items found on the web (L16). Without that analysis, the claim is not supported.
:::
::::

The second half of the lesson looks inside models. A model with $d$ dimensions in its residual stream may represent many more than $d$ features, as directions that overlap a little. The widget plants sparse features in a small space and trains a sparse autoencoder to find them again.

:::widget{name=FeatureDictionary features=4 latents=8}
:::

::::predict{id=p2 kind=numeric answer=0.1 tol=0.01}
Two random directions in 100 dimensions have a squared cosine of $1/100$ on average. What is the typical size of their cosine (the root mean square)?

:::reveal
$\sqrt{1/100} = 0.1$: random directions in high dimensions are nearly orthogonal. In a residual stream of a few thousand dimensions the typical overlap is about 0.02, so a model can pack far more directions than dimensions with little interference between features that are rarely active together. This is superposition, and it is why single neurons are often hard to interpret.
:::
::::
