# How much the prior matters

For a test with sensitivity $s$ and false-positive rate $f$, the posterior after one positive is $p(\pi) = \frac{s\pi}{s\pi + f(1 - \pi)}$ as a function of the prior $\pi$.

- `post(pi, s, f)`: that function.
- `dpost_dprior(pi, s, f)`: its derivative, $\frac{sf}{(s\pi + f(1 - \pi))^2}$ by the quotient rule (M15).
- `prior_needed(target, s, f)`: the prior at which the posterior equals `target`, by solving the equation for $\pi$ (it is linear in the odds: posterior odds $= \frac sf \times$ prior odds).

The tests run a **gradient check** of `dpost_dprior` against central differences. Near $\pi = 0$ the slope is $s/f$: for a rare condition the posterior is almost proportional to the prior, which is why getting the base rate right matters so much.

## Hints

1. Quotient rule: numerator $s\pi$, denominator $s\pi + f(1 - \pi)$.
2. Odds: $o = \pi/(1 - \pi)$; the posterior odds are $\frac sf o$.
3. Convert target odds back to a prior: $\pi = o/(1 + o)$.
