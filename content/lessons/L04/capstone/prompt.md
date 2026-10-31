# Capstone: your engine against PyTorch

Open the Colab notebook for this lesson. It runs on any runtime, CPU included.

1. Paste your finished engine from exercise 9 into the first code cell.
2. Train a `2-64-3` ReLU network on the spiral for 300 full-batch steps at learning rate 1 with your engine, and build the same network in PyTorch from the same initial weights (`nn.Linear` stores the weight transposed). Train it with `torch.optim.SGD` and `F.cross_entropy` in float64. The two loss curves must agree within $10^{-6}$ at every step.
3. Write `walk_grad_fn(t)`, which lists the class names of every function in `t.grad_fn`'s graph, and run it on the PyTorch loss.
4. Implement the squared ReLU as a `torch.autograd.Function` with your own backward rule, and check it with `torch.autograd.gradcheck`.

Run the autograder cell at the end and paste the completion code here.
