# Puzzle: three directions out of 768

Two thousand sentence embeddings, each 768 numbers. Plotting them is impossible, yet a few directions in that space carry most of the differences between them. How do you find those directions, and how many you need?

::::predict{id=p1 kind=choice answer=c}
Which directions capture the most variation in the data?

- The coordinate axes with the largest values.
- The directions of the individual embeddings with the largest lengths.
- The top singular vectors of the data matrix after subtracting the mean, equivalently the top eigenvectors of its covariance matrix.
- Random directions: in high dimension they are all the same.

:::reveal
The top right singular vectors of the centred data matrix. The first is the unit direction along which the projections of the points spread out the most; the next is the most spread direction perpendicular to it, and so on. This is **principal component analysis**. Without subtracting the mean, the first direction would mostly point at the mean, as Movement 5 shows.
:::
::::

::::predict{id=p2 kind=numeric answer=0.929 tol=0.005}
The centred data have singular values 30, 20, 10 and then values too small to matter. The variance along each direction is proportional to the square of its singular value. What fraction of the variance do the top two directions explain?

:::reveal
$(900 + 400) / (900 + 400 + 100) = 1300 / 1400 \approx 0.929$. Squares make the top values dominate: a singular value three times smaller carries nine times less variance. Keeping two of the 768 directions keeps 93 percent of the variation.
:::
::::

The bars are the singular values of a data matrix with three planted directions and noise. Keep the top $k$ and read the explained fraction. Raise the noise until the planted directions disappear among the rest.

:::widget{name=SpectrumBars rank=3 noise=0.3 k=3}
:::

## Questions to carry into the derivation

1. What factorization works for every matrix, square or not?
2. Why are the singular values the axes of an ellipse?
3. Why is cutting the SVD the best possible compression?
4. How many directions are enough, and how would you decide?
