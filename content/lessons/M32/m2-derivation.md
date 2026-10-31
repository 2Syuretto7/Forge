# Derivation: Markov chains and MCMC

## 1. The Markov property and transition matrices

A sequence of random states $X_0, X_1, \dots$ is a **Markov chain** when the next state depends on the past only through the present:

$$
P(X_{t+1} = j \mid X_t = i, X_{t-1}, \dots, X_0) = P(X_{t+1} = j \mid X_t = i) = P_{ij} .
$$

On finitely many states the probabilities $P_{ij}$ form the **transition matrix**: nonnegative entries, each row summing to 1. Write the distribution of $X_t$ as a row vector $\pi_t$. Conditioning on the current state gives $\pi_{t+1} = \pi_tP$, so $\pi_t = \pi_0P^t$, and $(P^t)_{ij}$ is the chance of going from $i$ to $j$ in exactly $t$ steps. The weather chain: a sunny day is followed by sun with probability $0.9$, a rainy day by sun with probability $0.5$.

$$
P = \begin{pmatrix} 0.9 & 0.1 \\ 0.5 & 0.5 \end{pmatrix} .
$$

::::derivation{id=d1 title="Two days ahead"}
:::step
Sunny today, the chance of sun the day after tomorrow is $(P^2)_{00} = 0.9 \times 0.9 + 0.1 \times 0.5 =$ [[0.86]].
:::
::::

## 2. Stationary distributions

A distribution with $\pi P = \pi$ is **stationary**: a chain started there stays there. Transposed, $P^\top\pi^\top = \pi^\top$, so $\pi$ is an eigenvector of $P^\top$ with eigenvalue 1, the left eigenvector of $P$ that M13 met at the end of its derivation. One always exists: the rows of $P$ sum to 1, so $P\mathbf 1 = \mathbf 1$, and $P$ and $P^\top$ share eigenvalues.

:::edge{from=M13 text="a stationary distribution is an eigenvector with eigenvalue 1."}
:::

When is it unique, and does every start reach it? Two conditions suffice on a finite chain. **Irreducible**: every state can reach every other. **Aperiodic**: the possible return times to a state have greatest common divisor 1. Under both, the Perron-Frobenius theorem makes the eigenvalue 1 simple and every other eigenvalue smaller than 1 in modulus, so $\pi_0P^t \to \pi$ from every $\pi_0$, which is the power method of M13 running on its own. The **ergodic theorem** adds what sampling needs: the time average $\frac1n\sum_{t<n}f(X_t)$ of one long path converges to $\sum_i\pi_if(i)$.

For two states, $P = \begin{pmatrix} 1 - a & a \\ b & 1 - b\end{pmatrix}$, the flow from state 0 to state 1 must equal the flow back: $\pi_0a = \pi_1b$.

::::derivation{id=d2 title="The two-state chain"}
:::step
With $a = 0.1$ and $b = 0.5$, the long-run fraction of sunny days is $\pi_0 = b/(a + b) \approx$ [[0.8333|tol=0.001]].
:::
:::step
The other eigenvalue of $P$ is its trace minus 1, $1 - a - b =$ [[0.4]], so the distance to $\pi$ shrinks by that factor each day.
:::
::::

## 3. Detailed balance

A distribution $\pi$ satisfies **detailed balance** with $P$ when

$$
\pi_iP_{ij} = \pi_jP_{ji} \quad \text{for all } i, j :
$$

in the long run, the flow of probability from $i$ to $j$ equals the flow back. Summing over $i$ gives $\sum_i\pi_iP_{ij} = \pi_j\sum_iP_{ji} = \pi_j$: detailed balance implies stationarity. The converse fails: a chain that walks clockwise round a ring has the uniform distribution as stationary, but all its flow goes one way. Chains with detailed balance are called **reversible**, because the path run backwards has the same law. Their matrices are symmetric after the change of basis $D^{1/2}PD^{-1/2}$ with $D = \operatorname{diag}(\pi)$, so all their eigenvalues are real (M13's spectral theorem).

Detailed balance is a local condition, one pair of states at a time. That is what makes it the tool for building chains with a prescribed stationary distribution.

## 4. Mixing and the spectral gap

How close is $\pi_t$ to $\pi$? Measure with the **total variation distance** $\lVert\mu - \nu\rVert_{TV} = \frac12\sum_i\lvert\mu_i - \nu_i\rvert$, the largest difference in probability the two distributions assign to any event. Expand the starting distribution in the eigenvectors of $P$: the component along $\pi$ never changes, and every other component is multiplied by its eigenvalue at each step, so

$$
\lVert\pi_t - \pi\rVert_{TV} \le C\,\lambda_*^t, \qquad \lambda_* = \max\{\lvert\lambda\rvert : \lambda \ne 1\} .
$$

The **spectral gap** $1 - \lambda_*$ sets the speed. For a reversible chain the **mixing time**, the steps needed to bring the worst start within $\varepsilon$, obeys $t_{\text{mix}}(\varepsilon) \le \frac{\ln(1/(\varepsilon\pi_{\min}))}{1 - \lambda_*}$. A lazy random walk on a ring of $n$ states (stay with probability $\frac12$, step to each neighbour with probability $\frac14$) has eigenvalues $\frac12 + \frac12\cos(2\pi k/n)$, a gap of about $\pi^2/n^2$, and a mixing time that grows like $n^2$: a random walk needs $n^2$ steps to travel a distance $n$.

::::derivation{id=d3 title="The lazy ring"}
:::step
For $n = 20$ the gap is $\frac12(1 - \cos(2\pi/20)) \approx$ [[0.0245|tol=0.0005]].
:::
:::step
Its inverse, the **relaxation time** over which the distance shrinks by a factor $e$, is about [[40.9|tol=0.5]] steps.
:::
::::

Shuffling is a random walk on the $52!$ orders of a deck. A riffle shuffle splits the order into at most two interleaved **rising sequences**, and $k$ riffles into at most $2^k$; Bayer and Diaconis showed that the probability of an order after $k$ riffles depends only on its number $r$ of rising sequences, $\binom{2^k + n - r}n/2^{kn}$, which gives the exact distance of the puzzle. Its shape, flat near 1 and then a sudden fall around $\frac32\log_2n \approx 8.6$ shuffles, is the **cutoff phenomenon**, common to many chains on large state spaces.

## 5. Metropolis-Hastings

Now reverse the question: given a target $\pi$, known perhaps only up to a constant, as a posterior is, build a chain whose stationary distribution is $\pi$. Start from any **proposal** $q(x, y)$, a way to suggest a move from $x$ to $y$, and accept the suggestion with probability $\alpha(x, y)$; on a rejection, stay at $x$. Detailed balance for $x \ne y$ asks

$$
\pi(x)\,q(x, y)\,\alpha(x, y) = \pi(y)\,q(y, x)\,\alpha(y, x) .
$$

The largest acceptance probabilities that satisfy it are

$$
\alpha(x, y) = \min\left(1, \frac{\pi(y)\,q(y, x)}{\pi(x)\,q(x, y)}\right) ,
$$

because then both sides equal $\min(\pi(x)q(x, y), \pi(y)q(y, x))$. Rejections only add to the chance of staying put, which detailed balance does not constrain. Only the ratio $\pi(y)/\pi(x)$ appears, so the normalizing constant, the integral that makes Bayesian posteriors hard, cancels. For a symmetric proposal, such as the random walk $y = x + s\,z$ with $z$ standard normal, the $q$ terms cancel too (**Metropolis**); for an asymmetric one the factor $q(y, x)/q(x, y)$ is the **Hastings correction**, and leaving it out makes the chain converge to the wrong distribution.

::::derivation{id=d4 title="Accepting a move"}
:::step
For the standard normal target and a symmetric proposal, the move from $x = 0$ to $y = 1$ is accepted with probability $e^{-1/2} \approx$ [[0.607|tol=0.001]].
:::
:::step
The move back, from $x = 1$ to $y = 0$, is accepted with probability [[1]].
:::
::::

The widget runs random-walk Metropolis on a target with two peaks. Watch the acceptance rate, the trace and the effective sample size as you change the step.

:::widget{name=MarkovChainSim logstep=0.3 sep=4 n=5000}
:::

The step size is the whole art of the random walk. In $d$ dimensions the best step shrinks like $2.38/\sqrt d$ times the target's scale, and the acceptance rate at the optimum tends to $0.234$, a theorem of Roberts, Gelman and Gilks. Tuning the step until about a quarter of proposals are accepted is the standard recipe.

## 6. Gibbs sampling

When every conditional distribution $\pi(x_i \mid x_{-i})$ can be sampled directly, update one coordinate at a time from its conditional. As a Metropolis-Hastings step with proposal $q(x, y) = \pi(y_i \mid x_{-i})$ for $y_{-i} = x_{-i}$, the ratio is

$$
\frac{\pi(y)\,\pi(x_i \mid x_{-i})}{\pi(x)\,\pi(y_i \mid x_{-i})} = \frac{\pi(x_{-i})\,\pi(y_i \mid x_{-i})\,\pi(x_i \mid x_{-i})}{\pi(x_{-i})\,\pi(x_i \mid x_{-i})\,\pi(y_i \mid x_{-i})} = 1 ,
$$

so every proposal is accepted. For a standard bivariate normal with correlation $\rho$ the conditionals are $x \mid y \sim N(\rho y, 1 - \rho^2)$, and one sweep gives $x_{t+1} = \rho^2x_t + \text{noise}$: an AR(1) chain with lag-one autocorrelation $\rho^2$. Strong correlation between coordinates makes Gibbs crawl.

::::predict{id=p3 kind=choice answer=b}
Gibbs sampling a bivariate normal with correlation $0.99$: what is the lag-one autocorrelation of the $x$ chain?

- $0.99$
- About $0.98$
- About $0.5$
- About $0.01$

:::reveal
$\rho^2 = 0.9801$. Each sweep keeps 98 percent of the previous value, so successive samples are nearly copies, and a run of 10,000 sweeps is worth only about 100 independent draws, as Section 7 computes. Rotating the coordinates to undo the correlation, or updating both together, fixes it.
:::
::::

## 7. Effective sample size

Averages along a chain converge to expectations, but slowly when successive samples are correlated. If the chain is stationary with variance $\sigma^2$ and lag-$k$ autocorrelation $\rho_k$, expanding the variance of the mean of $n$ samples (M22) gives

$$
\operatorname{Var}(\bar X) = \frac{\sigma^2}{n}\Big(1 + 2\sum_{k=1}^{n-1}\Big(1 - \frac kn\Big)\rho_k\Big) \approx \frac{\sigma^2}{n}\Big(1 + 2\sum_{k \ge 1}\rho_k\Big) .
$$

The chain is worth $n_{\text{eff}} = n/(1 + 2\sum_k\rho_k)$ independent samples, its **effective sample size**, and the **Monte Carlo standard error** of the mean is $\sigma/\sqrt{n_{\text{eff}}}$. Estimated autocorrelations at large lags are pure noise, so in practice the sum is cut off when the estimates turn negative. For an AR(1) chain $\rho_k = \phi^k$ and $1 + 2\sum_k\phi^k = (1 + \phi)/(1 - \phi)$.

::::derivation{id=d5 title="An AR(1) chain"}
:::step
For $\phi = 0.9$ the factor $(1 + \phi)/(1 - \phi)$ is [[19]].
:::
:::step
So 10,000 steps are worth about $10{,}000/19 \approx$ [[526|tol=1]] independent samples.
:::
::::

A single chain cannot reveal what it has not visited. Running several chains from scattered starting points and comparing the variance between them with the variance within them, the statistic $\hat R$, exposes chains stuck in different regions; values above about 1.01 mean the chains disagree.

## 8. Random walks, Brownian motion and Langevin dynamics

A $\pm1$ random walk $S_k$ has $\operatorname{Var}S_k = k$. Run it $n$ times faster and scale it by $1/\sqrt n$: $W(t) = S_{\lfloor nt\rfloor}/\sqrt n$ has variance close to $t$, is close to normal by the central limit theorem, and has independent increments. As $n \to \infty$ the whole path converges to **Brownian motion**, whose density at time $t$ is $p(x, t) = \frac1{\sqrt{2\pi t}}e^{-x^2/(2t)}$ and which solves the heat equation $\partial_tp = \frac12\partial_x^2p$: probability spreads like heat.

Add a drift up the gradient of a log density and the **Langevin diffusion** $dX = \nabla\log\pi(X)\,dt + \sqrt2\,dW$ has $\pi$ as its stationary distribution: its density evolves by $\partial_tp = -\nabla\cdot(p\nabla\log\pi) + \Delta p$, and at $p = \pi$ the right side is $-\nabla\cdot\nabla\pi + \Delta\pi = 0$. One Euler step gives the proposal $y = x + h\nabla\log\pi(x) + \sqrt{2h}\,z$. Used as it is, the **unadjusted Langevin algorithm** samples a slightly wrong distribution, too wide by a factor that grows with $h$; corrected by Metropolis-Hastings, it is **MALA**, which is exact, and whose best step shrinks only like $d^{-1/3}$, with an optimal acceptance rate near $0.574$.

Constant-step SGD is the same kind of chain. On $f(x) = \frac a2x^2$ with gradient noise of standard deviation $s$, the update $x' = x - \eta(ax + s\,z)$ is AR(1), and its stationary variance solves $v = (1 - \eta a)^2v + \eta^2s^2$:

$$
v = \frac{\eta s^2}{a(2 - \eta a)} \approx \frac{\eta s^2}{2a} .
$$

That is M29's noise floor, now seen as a stationary distribution: SGD samples from roughly $e^{-f/T}$ at a temperature $T = \eta s^2/2$ proportional to the step.

:::edge{from=M29 text="constant-step SGD is a Markov chain with a stationary distribution."}
:::

:::edge{to=M37 text="diffusion models run a Langevin-type chain from noise to data."}
:::

## Summary

| Idea | Statement | Use |
| --- | --- | --- |
| Markov chain | $\pi_{t+1} = \pi_tP$, rows of $P$ sum to 1 | distributions after $t$ steps |
| Stationary distribution | $\pi P = \pi$, the left eigenvector for eigenvalue 1 | long-run behaviour, ergodic averages |
| Detailed balance | $\pi_iP_{ij} = \pi_jP_{ji}$ implies stationarity | building samplers |
| Spectral gap | distance $\le C\lambda_*^t$; mixing time $\propto 1/(1 - \lambda_*)$ | how long to run |
| Metropolis-Hastings | accept with $\min(1, \pi(y)q(y, x)/(\pi(x)q(x, y)))$ | sampling unnormalized targets |
| Gibbs | sample each conditional; acceptance 1 | conditionally simple models |
| Effective sample size | $n/(1 + 2\sum_k\rho_k)$ | error bars for chain averages |
| Langevin | $y = x + h\nabla\log\pi + \sqrt{2h}\,z$; SGD variance $\eta s^2/(a(2 - \eta a))$ | gradient-based samplers, SGD noise |
