# Break it: too few items and probes that see everything

## Too few items

:::exercise{ref=e11}
:::

## A probe on noise

::::predict{id=p4 kind=choice answer=a}
A linear probe is trained on 100 examples of 200-dimensional random features with random labels. What training accuracy does it reach?

- 100%: with more dimensions than examples, some hyperplane separates any labelling.
- About 50%, since the labels are random.
- About 75%, half way between.
- It cannot be trained at all.

:::reveal
With $d \ge n$, $n$ points in general position can be separated in any way, so the probe fits the noise perfectly and is at chance on new data. Training accuracy measures the probe's capacity, not what the features contain. Report held-out accuracy, and compare with random features or a control task of the same size.
:::
::::

:::exercise{ref=e12}
:::

## What to take away

- Report every score with an interval over items, and compare models item by item.
- Check for contamination, fix the prompt format, and use enough items to resolve the differences you claim.
- A probe shows what is linearly decodable; selectivity and interventions show more.
- Look for features as directions, with sparse autoencoders, and test them by intervening.
- Patching locates components that carry a behaviour; a claim needs necessity, sufficiency and a random baseline.
