# Capstone: a diffusion model from scratch

The starter provides `sample_target(n, rng)`, a three-component mixture in the plane, and `sliced_w1(X, Y, seed=0)`, the distance of e09 with fixed projections.

1. `kde_score(X, t, centres, h)` and `dsm_loss(score, x0, seed, T=5.0, n_t=8)` as in e11, with the generator built from `seed`.
2. `fit(train, valid, hs=(0.0, 0.05, 0.1, 0.2, 0.4))`: the bandwidth with the smallest held-out loss.
3. `sample(train, h, n, seed=0, T=5.0, steps=60)`: the reverse SDE from $N(0, I)$ on a geometric grid down to $10^{-3}$, with the kernel score.
4. `nn_distance(gen, train)` as in e15.
5. `REPORT`: at least 120 words. Report the chosen bandwidth and the held-out losses, the sliced distance of your samples to fresh data against the distance of pure noise and of fresh data itself, the nearest-neighbour check for memorization, and how the model would change if it were a neural network.

The tests train on 300 points, validate on 300 and generate 600. A model cannot know more than its data, so the threshold is relative: the sliced distance from your samples to 2,000 fresh target points must be within 25 percent of the training set's own distance to them (about 0.17; pure noise is above 0.5). The tests also require a bandwidth above 0, and generated points no closer to the training set than 70 percent of the distance of fresh data.
