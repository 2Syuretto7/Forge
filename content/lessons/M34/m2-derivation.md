# Derivation: high-dimensional geometry and random matrices

## 1. Norms concentrate

Let $x \in \mathbb R^d$ have independent standard normal entries. Then $\lVert x\rVert^2 = \sum_ix_i^2$ is a sum of $d$ independent terms with mean 1 and variance 2, so

$$
\mathbb{E}\lVert x\rVert^2 = d, \qquad \operatorname{Var}\lVert x\rVert^2 = 2d .
$$

The relative spread of $\lVert x\rVert^2$ is $\sqrt{2/d}$, and since $\lVert x\rVert = \sqrt{\lVert x\rVert^2}$, the length is $\sqrt d$ give or take about $1/\sqrt2$, a spread that does not grow with $d$. Chernoff's method (M31) makes this exponential: the chance that $\lVert x\rVert^2$ misses $d$ by a fraction $\varepsilon$ falls like $e^{-d\varepsilon^2/8}$. A Gaussian in high dimension is a thin shell of radius $\sqrt d$, not a ball, and the same holds for distances between random points.

:::edge{from=M31 text="Chernoff's method on a sum of squares."}
:::

::::derivation{id=d1 title="A thin shell"}
:::step
In $d = 1000$ dimensions, $\lVert x\rVert^2$ has mean 1,000 and standard deviation $\sqrt{2000} \approx 44.7$.
:::
:::step
So $\lVert x\rVert \approx 31.6$, with a standard deviation of about $44.7/(2 \times 31.6) \approx$ [[0.707|tol=0.01]].
:::
::::

## 2. Random directions are nearly perpendicular

For independent $x, y$ with standard normal entries, $x\cdot y = \sum_ix_iy_i$ is a sum of $d$ independent terms with mean 0 and variance 1: mean 0, variance $d$. Divide by the two lengths, each about $\sqrt d$, and

$$
\cos\theta = \frac{x\cdot y}{\lVert x\rVert\lVert y\rVert} \approx N\Big(0, \frac1d\Big) .
$$

The angle is $90°$ with a spread of $\frac{180}{\pi\sqrt d}$ degrees. The dot product of M09, which in the plane takes every value between $\pm\lVert x\rVert\lVert y\rVert$, is in high dimension almost always a vanishing fraction of it. A consequence with practical weight: a $d$-dimensional space holds exponentially many nearly orthogonal directions, far more than $d$ exactly orthogonal ones, which is part of why embeddings can store many more features than they have dimensions.

The argument used independence and isotropy. Vectors that share a common component, as many learned embeddings do, have cosines far from 0 until the component is removed (e15).

::::derivation{id=d2 title="The puzzle's spread"}
:::step
In $d = 4096$ dimensions the cosine's standard deviation is $1/\sqrt{4096} \approx$ [[0.0156|tol=0.0005]].
:::
:::step
In degrees, $57.3/64 \approx$ [[0.895|tol=0.01]].
:::
::::

## 3. Why attention divides by the square root of $d$

An attention score is a dot product $q\cdot k$ of a query and a key. If their entries are roughly independent with variance 1, then by Section 2 the scores have variance $d$. For $d = 1024$ that is a standard deviation of 32: among 64 keys the top score typically exceeds the second by several units, the softmax $p_i = e^{z_i}/\sum_je^{z_j}$ puts nearly all its weight on one key, and its Jacobian

$$
\frac{\partial p}{\partial z} = \mathrm{diag}(p) - pp^\top
$$

is nearly zero when $p$ is nearly one-hot: the gradient stops flowing into the scores. Dividing by $\sqrt d$ makes the score variance 1 at every width, so the softmax behaves the same in a small model and a large one.

:::edge{to=L09 text="near-orthogonality explains the 1/sqrt(d) in attention."}
:::

::::derivation{id=d3 title="Unscaled scores"}
:::step
At $d = 1024$ the unscaled scores have standard deviation [[32]].
:::
::::

## 4. The Johnson-Lindenstrauss lemma

**Lemma.** For any $n$ points in $\mathbb R^d$ and $0 < \varepsilon < 1$, if $k \ge \frac{4\ln n}{\varepsilon^2/2 - \varepsilon^3/3}$, a random $d \times k$ matrix $R$ with independent $N(0, 1/k)$ entries maps the points so that every squared distance changes by a factor between $1 - \varepsilon$ and $1 + \varepsilon$, with probability at least $1/n$; with $6\ln n$ in place of $4\ln n$, with probability at least $1 - 1/n$.

**Proof.** Fix one difference $x = x_i - x_j$. Each coordinate of $R^\top x$ is $N(0, \lVert x\rVert^2/k)$, independent of the others, so $Z = k\lVert R^\top x\rVert^2/\lVert x\rVert^2$ is a sum of $k$ squared standard normals, $\chi^2_k$, with $\log\mathbb{E}e^{tZ} = -\frac k2\log(1 - 2t)$. Markov's inequality on $e^{tZ}$ (M31) and the best $t = \frac{\varepsilon}{2(1 + \varepsilon)}$ give

$$
P\big(Z \ge (1 + \varepsilon)k\big) \le \big((1 + \varepsilon)e^{-\varepsilon}\big)^{k/2} \le e^{-\frac k2(\varepsilon^2/2 - \varepsilon^3/3)} ,
$$

using $\log(1 + \varepsilon) \le \varepsilon - \varepsilon^2/2 + \varepsilon^3/3$; the lower tail obeys a bound at least as small. Each of the $\binom n2$ pairs fails with probability at most $2e^{-\frac k2(\varepsilon^2/2 - \varepsilon^3/3)}$, and with the stated $k$ this is at most $2/n^2$, so the union bound puts the total below $\binom n2\cdot\frac2{n^2} = \frac{n - 1}n < 1$: a good projection exists, and a random one is good with probability at least $1/n$. With $6\ln n$ the per-pair bound is $2/n^3$ and the total below $1/n$. The original dimension $d$ never appears. $\square$

The same matrix is the test matrix of M33's range finder: a random projection preserves the geometry of a low-dimensional subspace, which is why the range finder captures the top singular directions.

:::edge{from=M33 text="randomized SVD works because random projections preserve geometry."}
:::

::::derivation{id=d4 title="Two hundred points"}
:::step
For $n = 200$ points and $\varepsilon = 0.3$, the lemma asks for $k = \lceil 4\ln 200/(0.045 - 0.009)\rceil =$ [[589]] dimensions, whether the points live in a thousand dimensions or a million.
:::
::::

## 5. Variance-preserving initialization

A linear layer $y = Wx$ with $n_{\text{in}}$ inputs and independent weights of mean 0 and variance $v$ gives each output $\operatorname{Var}y_i = n_{\text{in}}\,v\,\mathbb{E}x_j^2$, by Section 2's sum of independent terms. A ReLU keeps the positive half of a symmetric variable, so $\mathbb{E}\,\mathrm{relu}(y)^2 = \frac12\operatorname{Var}y$. Per layer, the second moment of the activations is multiplied by

$$
c = \tfrac12n_{\text{in}}v ,
$$

and after $L$ layers by $c^L$. **He initialization**, $v = 2/n_{\text{in}}$, makes $c = 1$; Xavier's $v = 1/n_{\text{in}}$ was derived for layers without the ReLU's halving and gives $c = \frac12$ when used with ReLUs. The backward pass multiplies gradient variances by $\frac12n_{\text{out}}v$, the same condition when the widths match. Normalization layers and residual connections are the architectural versions of the same requirement.

:::edge{to=L06 text="variance preservation is what initialization and normalization protect."}
:::

::::derivation{id=d5 title="Fifty layers at the wrong scale"}
:::step
With $c = \frac12$, fifty layers multiply the second moment by $2^{-50}$, whose base-10 logarithm is about [[-15.05|tol=0.05]].
:::
::::

## 6. The Marchenko-Pastur law and signals that escape it

Draw $n$ samples of $p$ independent standard normal features. The sample covariance $S = X^\top X/n$ estimates the identity, every eigenvalue 1; yet the sample eigenvalues spread out. As $n, p \to \infty$ with $p/n \to \gamma \in (0, 1]$, their histogram approaches the **Marchenko-Pastur** density

$$
f(\lambda) = \frac{\sqrt{(\lambda_+ - \lambda)(\lambda - \lambda_-)}}{2\pi\gamma\lambda}, \qquad \lambda_\pm = (1 \pm \sqrt\gamma)^2 ,
$$

with mean 1 and second moment $1 + \gamma$. With four samples per feature, $\gamma = \frac14$, the eigenvalues fill $[0.25, 2.25]$: a ninefold spread from pure noise. Directions in which the sample variance looks large or small may be nothing but sampling error.

::::predict{id=p3 kind=choice answer=c}
1,600 samples of 400 independent features with variance 1, so every true eigenvalue is 1. Between which values do the sample covariance's eigenvalues lie?

- Between $0.95$ and $1.05$.
- Between $0.75$ and $1.25$.
- Between $0.25$ and $2.25$.
- Between $0$ and $10$.

:::reveal
Between $0.25$ and $2.25$, the Marchenko-Pastur edges for $\gamma = 400/1600 = \frac14$. Each entry of $S$ is estimated well, but 400 eigenvalues estimated from 1,600 samples are not: the errors in its roughly $80{,}000$ distinct entries conspire.
:::
::::

Now plant a real signal: one direction with variance $1 + \ell$. Baik, Ben Arous and Péché showed a sharp **BBP transition**: if $\ell \le \sqrt\gamma$ the top sample eigenvalue sticks to the bulk edge and its eigenvector carries no information about the signal; if $\ell > \sqrt\gamma$ it separates, at $(1 + \ell)(1 + \gamma/\ell)$, and its eigenvector's squared overlap with the true direction tends to $\frac{1 - \gamma/\ell^2}{1 + \gamma/\ell}$.

:::widget{name=RandomSpectrum p=100 gamma=0.25 spike=0}
:::

## 7. Spectra of trained weights

At initialization a weight matrix is a random matrix, and the spectrum of $W^\top W$ follows Marchenko-Pastur. Training changes it in two visible ways: eigenvalues escape above the bulk, one for each direction the layer has learned strongly enough to clear the BBP threshold, and the bulk itself develops a heavy tail as many weaker correlations accumulate. Counting the eigenvalues beyond the edge, as in e09, is a quick measure of how much structure a layer holds, and comparing a layer's spectrum with the Marchenko-Pastur fit for its shape tells signal from the noise of finite width.

:::edge{to=M38 text="the geometry and spectra of high-dimensional models."}
:::

## Summary

| Idea | Statement | Use |
| --- | --- | --- |
| Norms | $\lVert x\rVert \approx \sqrt d \pm 1/\sqrt2$ | thin shells, distance concentration |
| Angles | $\cos\theta \approx N(0, 1/d)$ | near-orthogonality |
| Attention | $\operatorname{Var}(q\cdot k) = d$; divide by $\sqrt d$ | unsaturated softmax |
| Johnson-Lindenstrauss | $k \ge 4\ln n/(\varepsilon^2/2 - \varepsilon^3/3)$ | dimension reduction, sketching |
| Initialization | per-layer factor $\frac12n_{\text{in}}v$; He: $v = 2/n_{\text{in}}$ | stable deep networks |
| Marchenko-Pastur | eigenvalues fill $[(1 - \sqrt\gamma)^2, (1 + \sqrt\gamma)^2]$ | noise floor of a spectrum |
| BBP | a spike escapes only if $\ell > \sqrt\gamma$ | detecting real structure |
