# Capstone: a diffusion model from scratch

Build a complete diffusion model in NumPy for a three-component mixture in the plane: a kernel score model of 300 training points, its bandwidth chosen by denoising score matching on held-out data, and the reverse-time SDE to generate 600 new points from noise. Score the result with a sliced Wasserstein distance against fresh data, compare it with what the training data alone achieve, and check that the model generates new points rather than copies.

:::exercise{ref=capstone}
:::

## When you finish

You can write down a diffusion model from its mathematics: the forward SDE, the score, the objective that learns it, and the reverse process that uses it. M38 asks you to derive a real paper's equations the same way.

:::edge{to=M38 text="deriving and reproducing a real paper."}
:::
