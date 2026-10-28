# Break it: an fp16 softmax

1. `naive_softmax(x)`: exponentiate, sum and divide, entirely in the input's precision, without subtracting the maximum.
2. `stable_softmax(x)`: subtract the row maximum, exponentiate and sum in float32, and return the result in the input's precision.
3. `overflow_threshold(dtype=np.float16)`: the largest $x$ with finite $e^x$ in that precision.

Then feed both a row of fp16 attention scores containing a 12.

## Hints

1. `np.finfo(np.float16).max` is 65504.
2. Pass `dtype=x.dtype` to the sum in the naive version so it really accumulates in fp16.
3. The stable version never exponentiates anything larger than 0.
