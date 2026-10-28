# Superposition

A model with $d$ dimensions can store far more than $d$ features if they are rarely active together, by giving them nearly orthogonal directions. The price is interference: reading one feature picks up a little of the others.

1. `random_unit_vectors(n, d, seed=0)`.
2. `mean_interference(V)`: the mean squared cosine between distinct rows.
3. `max_interference(V)`: the largest absolute cosine between distinct rows.

## Hints

1. The Gram matrix $V V^\top$ holds all the cosines; its diagonal is 1.
2. Random directions have mean squared cosine $1/d$: high dimensions make near-orthogonality cheap.
3. This is why individual neurons are often polysemantic, and why sparse autoencoders (exercise 7) look for directions instead.
