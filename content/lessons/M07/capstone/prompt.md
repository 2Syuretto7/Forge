# Capstone: a rotary position-encoding toy

Write the rotary encoding with complex numbers, prove its key property, and check it.

Treat a vector of even length $d$ as $d/2$ complex numbers $z_j = x_{2j} + i\,x_{2j+1}$. Encoding at position $m$ multiplies each by $e^{i m \omega_j}$ with $\omega_j = 10000^{-2j/d}$.

- `to_complex(x)` and `from_complex(z)`: convert between a real list of even length and a list of complex numbers.
- `encode(x, m)`: the encoded real vector.
- `score(q, k, m, n)`: the real dot product of the encoded query and key.
- `score_from_offset(q, k, offset)`: the same score computed **only** from the offset $m - n$: the real part of $\sum_j z_j \overline{w_j} e^{i (m - n) \omega_j}$, where $z$ and $w$ are the complex forms of `q` and `k` and the bar is the complex conjugate.
- `verify(pairs, d, seed=0)`: draw `pairs` random queries, keys and positions, and return the largest absolute difference between `score` and `score_from_offset`.

Then fill in `PROOF`: at least 60 words explaining why the score depends only on $m - n$. Use the facts that the real dot product of two vectors written as complex numbers is $\operatorname{Re} \sum z_j \overline{w_j}$, and that $\overline{e^{i\alpha}} = e^{-i\alpha}$.

The tests check every function, require the difference over 1,000 pairs in 64 dimensions to stay below $10^{-9}$, and check that the proof uses the conjugate.
