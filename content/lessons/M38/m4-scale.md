# Scale: ranks, curvatures and comparisons

::::predict{id=p4 kind=choice answer=b}
DPO on 8 responses with 20,000 simulated comparisons: how far, in total variation, does the trained policy end from the KL-optimal policy the derivation predicts?

- About 0.3.
- About 0.03.
- About 0.0003.
- Exactly 0.

:::reveal
About 0.03 (0.032 in the capstone's reproduction), against 0.44 for the reference policy it started from. The remaining gap is sampling noise in the 20,000 comparisons; it shrinks like one over the square root of their number.
:::
::::

:::exercise{ref=e09}
:::

:::exercise{ref=e13}
:::
