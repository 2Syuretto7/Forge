# Explain it plainly: evaluating and reading a model

Explain to an engineer who ships models how to tell whether one model is really better than another, and how researchers find out what a model is doing inside.

- Write 150 to 400 words.
- Explain confidence intervals over items and paired comparisons.
- Explain what a linear probe shows and what it does not.
- Explain superposition, sparse autoencoders, and activation patching.

:::feynman{id=f1 prompt="Explain how to tell whether one model is really better than another on a benchmark, and how linear probes, sparse autoencoders and activation patching reveal what a model computes, including the limits of each." key_points="A benchmark score is an average over sampled items, so it needs a confidence interval over items, and two models should be compared item by item because they share hard items|Contamination, prompt format and seeds can move scores, so they must be checked and reported|A linear probe shows that a property is linearly decodable from activations, not that the model uses it, and needs a random-feature or control-task baseline|Superposition stores more features than dimensions as nearly orthogonal directions, so a sparse autoencoder with an L1 penalty and unit-norm decoder rows is used to recover feature directions|Activation patching replaces one component's activation with its value from another input and measures how much of the output difference it restores, which tests whether the component carries the behaviour"}
:::
