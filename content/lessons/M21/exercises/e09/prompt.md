# What a test result is worth

From a confusion matrix of counts `tp`, `fn`, `fp`, `tn`:

- `rates(tp, fn, fp, tn)`: a dictionary with `"sensitivity"` $= \frac{tp}{tp + fn}$, `"specificity"` $= \frac{tn}{tn + fp}$, `"ppv"` (positive predictive value, $P(\text{ill} \mid +)$) $= \frac{tp}{tp + fp}$ and `"npv"` $= \frac{tn}{tn + fn}$.
- `ppv_at(prevalence, sensitivity, specificity)`: the positive predictive value in a population with a different prevalence, by Bayes' rule.

The sensitivity and specificity belong to the test; the predictive values belong to the test **and** the population. A study in a hospital (high prevalence) overstates how much a positive means in a screening of the general public.

## Hints

1. Plain ratios of counts.
2. $\text{ppv} = \frac{s\pi}{s\pi + (1 - \text{spec})(1 - \pi)}$.
3. Check: the hospital's own prevalence, $\frac{tp + fn}{\text{total}}$, reproduces its own PPV.
