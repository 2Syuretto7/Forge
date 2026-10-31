# Build: deduplication and filtering

## Exact and near duplicates

:::exercise{ref=e01}
:::

:::exercise{ref=e02}
:::

:::exercise{ref=e03}
:::

:::exercise{ref=e04}
:::

:::exercise{ref=e05}
:::

## Quality

:::exercise{ref=e06}
:::

::::predict{id=p3 kind=choice answer=c}
A quality classifier is trained to separate Wikipedia articles (label 1) from random crawl pages (label 0), and you keep pages scoring above 0.5. Which good text is most at risk of being removed?

- Well-edited encyclopedic text.
- Spam.
- Good writing in styles absent from Wikipedia, such as dialogue, poetry or informal forums.
- Nothing: a classifier with high accuracy only removes junk.

:::reveal
The classifier learns what the reference looks like, not what quality is. Text far from the reference in style or dialect scores low however good it is, so aggressive classifier filtering narrows the distribution. Combine classifiers with rules, keep documents stochastically rather than by a hard cutoff, and check what was removed.
:::
::::

:::exercise{ref=e07}
:::
