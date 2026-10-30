# How long must a hash be?

A deduplication pipeline hashes every document and treats equal hashes as duplicates. A collision silently deletes a document.

- `bits_needed(n, p)`: the smallest whole number of bits $b$ with $\binom{n}{2} / 2^b \leq p$, for `n` documents and a tolerated collision probability `p` (the expected number of colliding pairs bounds the probability of any collision: the union bound).
- `max_documents(bits, p)`: the largest $n$ with $\binom{n}{2} / 2^{\text{bits}} \leq p$, by solving $n(n-1)/2 \leq p\,2^{\text{bits}}$ and checking the neighbours.

The tests size a hash for a billion documents at a one-in-a-million risk, and check the 64-bit hash's capacity.

## Hints

1. $b \geq \log_2 \binom{n}{2} - \log_2 p$; take the ceiling and check.
2. $n \approx \sqrt{2 p\, 2^{\text{bits}}}$.
3. Use exact integers where you can: `math.comb(n, 2)`.
