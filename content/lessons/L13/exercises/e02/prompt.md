# Range and precision of a format

1. `format_properties(exp_bits, man_bits)`: a dictionary with the largest finite value `"max"`, the smallest positive normal `"min_normal"`, the smallest positive subnormal `"min_subnormal"` and the machine epsilon `"eps"`.
2. `decimal_digits(man_bits)`: about how many significant decimal digits the format keeps, $(m + 1)\log_{10} 2$.

## Hints

1. Bias $= 2^{e-1} - 1$; the largest exponent of a finite number is $2^e - 2 - \text{bias}$.
2. The largest finite value is $(2 - 2^{-m}) \cdot 2^{e_{\max}}$.
3. The smallest subnormal is the smallest normal times $2^{-m}$.
