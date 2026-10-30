# Scale: a vocabulary of 50,000 and the limits of exp

A language model's last step is a softmax over its vocabulary, tens of thousands of entries. Its loss on a token is minus the log of the probability it gave the right one. Both are this lesson at scale.

## The loss of a model that knows nothing

A model whose scores are all equal gives every token probability $1/V$. Its loss is $-\ln(1/V) = \ln V$.

:::exercise{ref=e10}
:::

## Where exp overflows

::::predict{id=p4 kind=numeric answer=88.7 tol=1}
A 32-bit float holds numbers up to about $3.4 \times 10^{38}$. Above what value of $x$ does $e^x$ overflow to infinity in float32?

:::reveal
$\ln(3.4 \times 10^{38}) = 38 \ln 10 + \ln 3.4 \approx 87.5 + 1.2 = 88.7$. Logits above 89 are routine in a large model's softmax, so a softmax that exponentiates raw logits in float32 fails on real data. In float64 the threshold is about 709.8; in float16 it is just 11.1.
:::
::::

:::exercise{ref=e11}
:::

## Reading laws off log axes

The loss-curve dataset in the widget is $1.7 + 8 n^{-0.3}$: a power law plus a floor. Try the log-log axes. It is nearly straight but not quite, because of the floor. M35 fits such curves properly.

:::widget{name=LogScaler data=loss xlog=true ylog=true}
:::

:::exercise{ref=e12}
:::
