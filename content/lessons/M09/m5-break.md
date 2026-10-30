# Break it: long vectors, zero vectors and a distance that is not one

## The raw dot product prefers long vectors

$x \cdot y = \|x\|\,\|y\|\cos t$. Rank documents by raw dot product and a long, barely related vector can beat a short, perfectly aligned one.

::::predict{id=p5 kind=choice answer=a}
A query $q = (1, 0)$. Document A is $(0.9, 0.1)$, nearly the same direction. Document B is $(5, 5)$, at $45^\circ$. Which ranks first by raw dot product, and which by cosine?

- B by dot product (5 against 0.9), A by cosine (0.99 against 0.71).
- A by both.
- B by both.
- A by dot product, B by cosine.

:::reveal
$q \cdot A = 0.9$ and $q \cdot B = 5$, so B wins on the raw dot product purely by length. The cosines are $0.9/\|A\| \approx 0.994$ and $5/\|B\| \approx 0.707$, so A wins on direction. Retrieval systems normalize embeddings for exactly this reason, unless length is meant to carry information.
:::
::::

:::exercise{ref=e13}
:::

## The zero vector has no direction

:::exercise{ref=e14}
:::

## A distance that breaks the triangle inequality

$1 - \cos t$ is often called "cosine distance". It is not a distance in the mathematical sense, because it can violate the triangle inequality. The angle itself, $\arccos$ of the cosine, is a true distance on directions.

:::exercise{ref=e15}
:::

:::widget{name=VectorPlayground x1=2 x2=0 y1=0 y2=0.5}
:::

With the two arrows perpendicular, the dot product is 0 whatever their lengths. Shrink $y$ towards the origin: the angle stays $90^\circ$ until $y$ reaches zero, and then the caption has no angle to report.

## What to take away

- Normalize before comparing directions; keep raw dot products only when length means something.
- Guard the zero vector: there is no cosine with it.
- Check that a "distance" is a distance before an algorithm relies on the triangle inequality.
