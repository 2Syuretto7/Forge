# Build: models of GPU cost

These exercises turn the derivation into small tools you can apply to any kernel. They run in the browser; the measurements come in the Colab notebook.

## Counting and the roofline

:::exercise{ref=e01}
:::

:::exercise{ref=e02}
:::

## Tiling and occupancy

:::exercise{ref=e03}
:::

:::exercise{ref=e04}
:::

::::predict{id=p3 kind=choice answer=b}
A kernel uses blocks of 256 threads and 128 registers per thread on a T4 SM (65536 registers, at most 32 warps). What is its occupancy?

- 100 percent.
- 50 percent.
- 25 percent.
- 12.5 percent.

:::reveal
Each block needs $256 \cdot 128 = 32768$ registers, so only two blocks fit: 16 warps of the possible 32, an occupancy of 50 percent. Heavy register use is the most common occupancy limiter, and it is often worth it: registers are where tiled kernels keep their reused values.
:::
::::

## Fusion and the backward pass

:::exercise{ref=e05}
:::

:::exercise{ref=e06}
:::

:::exercise{ref=e07}
:::
