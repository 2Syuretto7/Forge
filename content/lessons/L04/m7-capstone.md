# Capstone: your engine against PyTorch

The capstone runs in Colab, where PyTorch is installed. You will paste your engine into the notebook, train the same two-layer network on the spiral with your engine and with PyTorch from identical initial weights, and show that the two loss curves agree to within $10^{-6}$ (both in float64). Along the way you will walk a real PyTorch `grad_fn` graph and write a custom `torch.autograd.Function` that passes PyTorch's own `gradcheck`.

This notebook does not need a GPU; a CPU runtime is fine.

:::exercise{ref=capstone}
:::

:::colab{notebook=L04 runtime=cpu}
:::

## When you finish

Your engine and PyTorch differ in speed, not in kind. PyTorch's tensors live on GPUs, its backward rules are C++ and CUDA kernels, and its graph records thousands of operations per step. L07 asks what each of those operations costs on a GPU, and why launching many small ones is slow.

:::edge{to=L07 text="What each recorded operation costs on a GPU."}
:::

:::edge{to=L05 text="Optimizers that consume your engine's gradients."}
:::
