# Explain it plainly: the dot product

Explain what a dot product measures to a 12-year-old, without a formula.

Guidelines:

- Write 150 to 400 words.
- Use a physical picture: pushing a cart at an angle, shadows, two people walking in nearly the same direction.
- Say what a large, a zero and a negative dot product mean.
- Say why you divide by the lengths to compare directions.

:::feynman{id=f1 prompt="Explain what a dot product measures, without a formula." key_points="It measures how much two arrows point the same way, scaled by how long they are|It is largest when they point the same way, zero when they are at right angles, and negative when they point apart|It equals the length of one arrow times the length of the shadow the other casts on it|Long arrows give big dot products even when the directions barely agree, so to compare directions you divide by both lengths|The result, the cosine similarity, is how embeddings of words and documents are compared"}
:::

## A written proof

:::feynman{id=proof1 prompt="Prove the Cauchy-Schwarz inequality: for vectors x and y in any number of dimensions, |x . y| <= |x| |y|, and say exactly when equality holds." key_points="Considers the squared length of x - t y, which is never negative for any real t|Expands it with the properties of the dot product into a quadratic in t|Chooses the t that minimizes it, or argues from the discriminant, to get (x . y)^2 <= |x|^2 |y|^2|Handles the case y = 0 separately|Shows equality holds exactly when one vector is a multiple of the other"}
:::
