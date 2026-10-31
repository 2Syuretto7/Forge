# Puzzle: a film of noise, run backwards

Take a picture and, a thousand times over, shrink it slightly toward grey and add a little Gaussian noise. At the end it is static, indistinguishable from any other picture treated the same way.

::::predict{id=p1 kind=choice answer=c}
Can the film be run backwards, from static to a picture? What would you need at each frame?

- No: noise destroys information, so nothing can undo it.
- Yes, if you store the noise that was added at each step.
- Yes, if at each frame you know which way the density of noised pictures increases.
- Yes, but only for the picture you started with.

:::reveal
Yes, with the direction in which the density of noised pictures increases: the **score**. The single picture cannot be recovered, but new pictures from the same distribution can. Anderson showed in 1982 that a diffusion run backwards in time is another diffusion, whose drift contains that score. Learning the score at every noise level is all a diffusion model does.
:::
::::

::::predict{id=p2 kind=choice answer=b}
The forward process shrinks by $e^{-t}$ and adds noise so that the variance tends to 1. After time $t = 3$, what fraction of the original signal's size remains?

- About 50 percent.
- About 5 percent.
- About 0.5 percent.
- None at all.

:::reveal
About 5 percent: $e^{-3} \approx 0.05$. Noise has nearly taken over, and the distribution of the noised data is close to the standard Gaussian; a little more time and the difference is invisible. That is why sampling can start from pure noise.
:::
::::

## Questions to carry into the derivation

1. How do you write down a differential equation with noise in it, and simulate it?
2. Where does the noised data's distribution go, and how fast?
3. What is the score, and how can you learn it without knowing the density?
4. Why does the reverse-time process need exactly the score?
