# Capstone: compressing text, and how close entropy says you can get

The starter contains `CORPUS`, about 1,800 characters of English prose. You will build a Huffman code for its characters, compress it, and compare the result with three entropy estimates.

Implement:

1. `char_probs(text)`: a dict mapping each character to its relative frequency.
2. `huffman_code(probs)`: a dict mapping each character to a codeword string of `"0"` and `"1"`. Repeatedly merge the two least probable nodes (use `heapq` with a tie-breaking counter). With a single symbol, use the codeword `"0"`.
3. `encode(text, code)` and `decode(bits, code)`: decoding must invert encoding exactly.
4. `bits_per_char(text, code)`: the length of the encoding divided by the number of characters.
5. `unigram_entropy(text)` and `bigram_conditional_entropy(text)`: in bits per character, the plug-in entropy of single characters, and of a character given the previous one, $H(X_t \mid X_{t-1}) = H(X_{t-1}, X_t) - H(X_{t-1})$ over consecutive pairs.
6. `REPORT`: at least 80 words. Give the four numbers, explain why the Huffman rate sits between the unigram entropy and one bit above it, why the bigram figure is lower, and what a model that uses longer context (a language model) would do to the achievable rate.

The tests check that the code is prefix-free, that the Huffman rate equals the optimum computed independently, that the round trip is exact, and that the entropy estimates satisfy the bounds of Sections 2 and 6.
