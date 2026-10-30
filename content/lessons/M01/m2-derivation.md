# Derivation: numbers, units and estimates

This movement builds the tools in order: the kinds of numbers, place value and powers of ten, scientific notation, units, and finally the theory of estimates. Take it in sittings. Each section ends in a derivation you complete.

## 1. Why there are several kinds of number

Start with the counting numbers $1, 2, 3, \dots$. They are enough to count and add. They are not enough to undo things.

- To undo addition, you need subtraction, and $3 - 5$ has no counting-number answer. Allowing negatives and zero gives the **integers** $\dots, -2, -1, 0, 1, 2, \dots$.
- To undo multiplication, you need division, and $3 \div 4$ has no integer answer. Allowing fractions gives the **rationals**: every number $p/q$ with integers $p$ and $q \neq 0$.
- Lengths force one more step. A square of side 1 has a diagonal $d$ with $d^2 = 1^2 + 1^2 = 2$, and no fraction squares to exactly 2 (you will prove this in M03). Filling every such gap gives the **real numbers**, the points of a continuous line.

Each extension keeps every rule that already worked and adds an answer where there was none. That pattern (extend the numbers so the rules keep working) will return when you meet complex numbers in M07.

A computer cannot store most real numbers exactly, because their decimal expansions never end. It stores an approximation with a fixed number of significant digits. For now, keep the picture: an integer type stores whole numbers exactly up to a limit, and a floating-point type stores about 16 significant decimal digits (in 64 bits) of any size. Both limits will bite in Movement 5.

## 2. Place value and powers of ten

The numeral 4,096 means

$$
4{,}096 = 4 \times 10^3 + 0 \times 10^2 + 9 \times 10^1 + 6 \times 10^0 .
$$

Each position is worth ten times the one to its right. Here $10^n$ means ten multiplied by itself $n$ times, so $10^3 = 1{,}000$ has three zeros. Computers use the same idea with two in place of ten: $4{,}096 = 2^{12}$, a one followed by twelve zeros in binary.

Powers of ten obey rules you can derive by counting zeros.

::::derivation{id=d1 title="The rules for powers of ten"}
:::step
$10^a \times 10^b$ is a one with $a$ zeros times a one with $b$ zeros, which is a one with $a + b$ zeros. So $10^5 \times 10^3 = 10^{\,?}$ with exponent [[8]].
:::
:::step
Dividing removes zeros: $10^a / 10^b = 10^{a-b}$ when $a \geq b$. So $10^9 / 10^4 = 10^{\,?}$ with exponent [[5]].
:::
:::step
Apply the division rule with $a = b$: $10^a / 10^a = 1$ must equal $10^{a-a}$. So the only sensible definition of $10^0$ is [[1]].
:::
:::step
Apply it with $a = 0$: $10^0 / 10^b = 1/10^b$ must equal $10^{-b}$. So $10^{-3}$ is the fraction $1/1000$, which as a decimal is [[0.001]].
:::
::::

Negative exponents are not a new idea, only the old rule kept working: $10^{-3}$ means "divide by ten three times".

## 3. Scientific notation

Writing $299{,}792{,}458$ invites miscounting the digits. **Scientific notation** writes a number as a mantissa between 1 and 10 times a power of ten:

$$
299{,}792{,}458 = 2.99792458 \times 10^8 .
$$

The exponent says how big the number is; the mantissa says what it is to within that size. Multiplying is then easy: multiply mantissas, add exponents, and tidy up if the new mantissa is 10 or more.

$$
(3 \times 10^4) \times (5 \times 10^6) = 15 \times 10^{10} = 1.5 \times 10^{11} .
$$

:::edge{from=M06 text="the exponent in scientific notation is the base-10 logarithm, rounded down; M06 makes the logarithm a function in its own right."}
:::

The exponent alone is the **order of magnitude**. Two numbers with the same exponent are "the same size" in the sense that matters for estimates. A quantity known "to an order of magnitude" is known to within a factor of about 3 either way (since $\sqrt{10} \approx 3.16$, the midpoint between two powers of ten on a ladder of powers is about 3.16 times the lower one).

**Significant figures.** Writing $1.5 \times 10^{11}$ claims two significant figures: the truth lies between about $1.45$ and $1.55 \times 10^{11}$. Writing $1.50 \times 10^{11}$ claims three. Never report more digits than your inputs justify; an estimate built from guesses good to a factor of 2 deserves one significant figure at most.

**Relative error.** If an estimate $\hat x$ approximates a true value $x$, its relative error is $|\hat x - x| / |x|$. For estimates that can be off by large factors, a better measure is the **factor off**: $\max(\hat x / x,\ x / \hat x)$, which treats "twice too big" and "half too big" as equally bad. It is always at least 1, and it equals 1 only when the estimate is exact.

## 4. Ratios, rates and units

A rate is a ratio with units: 60 kilometres per hour, $10^{14}$ FLOPs per second, 4 bytes per number. Units behave like algebraic symbols: they multiply, divide and cancel.

$$
60\ \frac{\text{km}}{\text{h}} \times 3\ \text{h} = 180\ \text{km} .
$$

The hours cancel, leaving kilometres. That cancellation is a free error check. If you compute a time and the units come out as "FLOP squared per second", you multiplied where you should have divided. This technique is called **dimensional analysis**, and it catches more mistakes than any other single habit.

::::derivation{id=d2 title="Units that cancel"}
:::step
A day has 24 hours of 60 minutes of 60 seconds, so one day is $24 \times 60 \times 60 =$ [[86400]] seconds.
:::
:::step
A GPU sustains $10^{14}$ FLOP/s. In one hour (3,600 s) it performs $10^{14} \times 3600 = 3.6 \times 10^{\,?}$ FLOPs, exponent [[17]]. The seconds cancel.
:::
:::step
A model stores $7 \times 10^9$ numbers at 2 bytes each. Its size is $1.4 \times 10^{10}$ bytes. With a gigabyte defined as $10^9$ bytes, that is [[14]] GB.
:::
:::step
Dividing work by speed gives time: $\dfrac{3.6 \times 10^{17}\ \text{FLOP}}{10^{14}\ \text{FLOP/s}} =$ [[3600]] seconds, the hour you started with.
:::
::::

One unit trap is worth naming now. A **gigabyte** (GB) is $10^9$ bytes, but a **gibibyte** (GiB), the unit most operating systems and GPU tools actually report, is $2^{30} = 1{,}073{,}741{,}824$ bytes, about 7 percent more. The difference grows with each step up: a TiB is about 10 percent more than a TB.

## 5. The theory of estimates

A **Fermi estimate** (after the physicist Enrico Fermi, who was famous for them) breaks an unknown quantity into a product of factors you can guess:

$$
\text{GPU-hours} = \frac{\text{FLOPs per token} \times \text{tokens}}{\text{FLOP/s per GPU} \times 3600\ \text{s/h}} .
$$

Each factor is uncertain. How uncertain is the product?

**Work on the log scale.** The base-10 logarithm of a positive number is its exponent written as a decimal: $\log_{10} 1000 = 3$, $\log_{10} 2 \approx 0.301$, and $\log_{10} 2000 \approx 3.301$. (M06 builds the logarithm properly; for now it is "the exponent of 10".) The rule $10^a \times 10^b = 10^{a+b}$ says that logarithms turn products into sums:

$$
\log_{10}(x_1 x_2 \cdots x_n) = \log_{10} x_1 + \log_{10} x_2 + \dots + \log_{10} x_n .
$$

A factor known "to within a factor of $k$" has a logarithm known to within $\pm h$ with $h = \log_{10} k$. So the question becomes: if each of $n$ numbers is off by up to $\pm h_i$, how far off is their sum?

**Worst case.** If every error has the same sign, the errors add: the sum is off by $h_1 + h_2 + \dots + h_n$. For ten factors each good to a factor of 2, that is $10 \times 0.301 = 3.01$, a factor of $10^{3.01} \approx 1000$.

**Typical case.** Suppose each error is $+h_i$ or $-h_i$ with equal chance, independently of the others. Write the total error as $E = s_1 h_1 + \dots + s_n h_n$ with each sign $s_i = \pm 1$. Then

$$
E^2 = \sum_i s_i^2 h_i^2 + \sum_{i \neq j} s_i s_j h_i h_j = \sum_i h_i^2 + \sum_{i \neq j} s_i s_j h_i h_j .
$$

Each $s_i^2 = 1$. Each cross term $s_i s_j$ is $+1$ or $-1$ with equal chance, so across many estimates the cross terms average to zero. The **typical** size of $E$ (the square root of its average square) is therefore

$$
\sqrt{h_1^2 + h_2^2 + \dots + h_n^2} .
$$

Errors add in **quadrature**, like the sides of a right triangle, instead of in a straight line. For $n$ equal errors this is $\sqrt{n}\,h$ instead of $n h$. Independent errors partly cancel.

::::derivation{id=d3 title="Why ten rough factors are not hopeless"}
:::step
With $n$ factors each uncertain by $\pm h$ in log units, the worst-case error of the product is $n h$ and the typical error is [[sqrt(n)*h]].
:::
:::step
Take nine factors, each good to a factor of 2, so $h = \log_{10} 2$. The worst case is a factor of $2^9 =$ [[512]].
:::
:::step
The typical error is $\sqrt{9}\, h = 3h$, which is a factor of $10^{3 \log_{10} 2} = 2^3 =$ [[8]].
:::
:::step
For the error to be typical, the factors' errors must be [[word:independent/independent of each other/uncorrelated]]: if you are optimistic about every factor in the same direction, the worst case is what you get.
:::
::::

::::predict{id=p3 kind=choice answer=b}
You multiply four factors, each independently uncertain by a factor of 3. What is the typical uncertainty of the product?

- A factor of 3: the errors cancel completely.
- A factor of 9, since $\sqrt{4} = 2$ and $3^2 = 9$.
- A factor of 12, since $4 \times 3 = 12$.
- A factor of 81, since $3^4 = 81$.

:::reveal
In log units each factor is off by $h = \log_{10} 3$. The typical error of the sum of four is $\sqrt{4}\,h = 2h$, which is a factor of $3^2 = 9$. The worst case is $3^4 = 81$. Note that "a factor of 12" adds the factors instead of their logarithms, a mistake that mixes up the two scales.
:::
::::

This is the mathematical reason Fermi estimates work, and also the condition under which they fail: correlated errors. If you underestimate the number of tokens because you underestimate the model size (because the two are linked), the errors do not cancel.

:::edge{from=M08 text="counting outcomes produces the huge numbers this ladder of powers holds; M08 counts them exactly."}
:::

## 6. Counting the FLOPs of a model

Now the puzzle, properly. A dense layer of a neural network multiplies an input vector of length $n$ by a weight matrix with $m$ rows and $n$ columns, producing $m$ outputs. Each output is a sum of $n$ products, which takes $n$ multiplications and $n - 1$ additions; counting one more addition for the bias, call it $n$ multiply-adds. So

$$
\text{FLOPs}(m \times n \text{ matrix times a vector}) = 2 m n .
$$

The matrix has $mn$ parameters, so this is **2 FLOPs per parameter**. A model is a chain of such layers (plus cheaper elementwise operations), so a forward pass for one token costs about $2N$ FLOPs, where $N$ is the number of parameters. Attention over a long context adds more, and you will count it in L13; for prompts shorter than a few thousand tokens the $2N$ term dominates.

Training costs more. Backpropagation, which you will build in L07, computes for every weight matrix two products of the same size as the forward one: the gradient with respect to the layer's input (to pass backwards) and the gradient with respect to the weights (to update them). That is about $4N$ FLOPs more, for a total of

$$
\text{training FLOPs} \approx 6 N D ,
$$

where $D$ is the number of training tokens.

::::derivation{id=d4 title="FLOPs of layers and models"}
:::step
A layer with a $2048 \times 2048$ weight matrix has $2048^2 = 4{,}194{,}304$ parameters, so one token costs $2 \times 2048^2 =$ [[8388608]] FLOPs in it.
:::
:::step
A model with $N = 10^9$ parameters spends about $2N =$ [[2*10^9]] FLOPs per token in a forward pass.
:::
:::step
Training a model with $N = 10^8$ parameters on $D = 2 \times 10^9$ tokens costs about $6ND = 1.2 \times 10^{\,?}$ FLOPs, exponent [[18]].
:::
:::step
At a sustained $10^{14}$ FLOP/s, that run takes $1.2 \times 10^{18} / 10^{14} = 12{,}000$ seconds, which is $12000/3600 \approx$ [[3.33|tol=0.05]] GPU-hours.
:::
::::

That last number is worth a pause: a model with a hundred million parameters, of the size that was state of the art in 2018, now trains in an afternoon on one GPU. Orders of magnitude move fast, and the only way to keep up is to estimate.

:::edge{to=M35 text="compute budgets like 6ND become the x axis of scaling laws, plotted on log-log axes where power laws are straight lines."}
:::

## Summary

| Idea | Rule | Use |
| --- | --- | --- |
| Powers of ten | $10^a 10^b = 10^{a+b}$, $10^{-n} = 1/10^n$ | count zeros, never digits |
| Scientific notation | $m \times 10^e$, $1 \leq m < 10$ | multiply mantissas, add exponents |
| Factor off | $\max(\hat x / x,\ x / \hat x)$ | error of an estimate |
| Units | multiply, divide and cancel like symbols | catch wrong formulas |
| Typical error | $\sqrt{h_1^2 + \dots + h_n^2}$ in log units | independent errors partly cancel |
| Model FLOPs | $2N$ per token forward, $6ND$ to train | budgets for every later lesson |
