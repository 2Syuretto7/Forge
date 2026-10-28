# Temperature, top-k and top-p

1. `softmax_t(logits, T=1.0)`: the softmax of `logits / T`.
2. `top_k_filter(logits, k)`: keep the `k` largest logits, set the rest to `-inf`.
3. `top_p_filter(logits, p)`: keep the smallest set of tokens, in decreasing order of probability, whose probabilities sum to at least `p`; set the rest to `-inf`.
4. `sample(logits, rng, T=1.0, k=None, p=None)`: divide by the temperature, apply the filters that are given, and draw a token with `rng.choice`.

## Hints

1. `-inf` logits get probability exactly 0 in the softmax.
2. For top-p, sort probabilities in decreasing order and find where the cumulative sum first reaches `p` (`np.searchsorted`).
3. With `T` near 0 the distribution becomes one-hot on the argmax.
