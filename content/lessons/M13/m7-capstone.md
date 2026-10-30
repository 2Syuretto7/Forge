# Capstone: a PageRank engine

The starter builds a web of 300 pages in several communities, some with no outgoing links. Your engine computes PageRank by power iteration without ever forming a dense matrix, handles pages without links, stops at a tolerance, and reports how many steps it took. A reference ranking from a dense eigenvector computation checks the answer; the second eigenvalue of the dense Google matrix predicts the number of steps, and your count must match the prediction.

:::exercise{ref=capstone}
:::

## When you finish

You have computed the most famous eigenvector of the internet era. M14 extends the spectral theorem to every matrix, square or not; M23 finds the principal components of data as eigenvectors of a covariance matrix; M32 studies the mixing of Markov chains, where the second eigenvalue is the clock.

:::edge{to=M29 text="the eigenvalues of the Hessian set the step size and momentum of gradient descent."}
:::
