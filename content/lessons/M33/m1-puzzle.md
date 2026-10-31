# Puzzle: same arithmetic, ten times faster

Multiplying two $4096 \times 4096$ matrices takes $2 \times 4096^3 \approx 1.37 \times 10^{11}$ floating-point operations, whatever order the loops run in. Yet a carefully ordered loop runs ten or more times faster than the textbook triple loop on the same chip.

::::predict{id=p1 kind=numeric answer=683 tol=60}
In fp32, how many flops does this product do per byte of the minimal data it must read and write (each input read once, the output written once)?

:::reveal
About 683: $1.37 \times 10^{11}$ flops over $3 \times 4096^2 \times 4 \approx 2.0 \times 10^8$ bytes, which is $4096/6$. The work grows like $n^3$ and the data like $n^2$, so large products have plenty of arithmetic per byte, if the algorithm reuses what it reads.
:::
::::

::::predict{id=p2 kind=choice answer=c}
The textbook loop re-reads both operands of every multiply-add from main memory: 8 bytes for 2 flops. A T4 does $8.1 \times 10^{12}$ fp32 flops per second and moves $3.2 \times 10^{11}$ bytes per second. How fast can that loop run?

- At the peak, $8.1 \times 10^{12}$ flops per second.
- About half the peak.
- About $8 \times 10^{10}$ flops per second, a hundredth of the peak.
- About $10^9$ flops per second.

:::reveal
About $8 \times 10^{10}$: a quarter of a flop per byte times $3.2 \times 10^{11}$ bytes per second. The arithmetic units sit idle 99 percent of the time, waiting for data. The fix is not fewer flops but fewer trips to memory, which is what blocking does.
:::
::::

## Questions to carry into the derivation

1. How do you tell whether a computation is limited by arithmetic or by data movement?
2. How can a solver use only matrix-vector products and still be fast?
3. Why does multiplying by a random matrix find a matrix's important directions?
4. When does a faster algorithm give a wrong answer?
