# Capstone: a scaling law you can bet on

Fit the five-parameter loss surface to 48 small training runs, put bootstrap intervals on its exponents and on the prediction for a run with about 38 times more compute, and check the prediction against the run's actual loss. Report what the fit implies for splitting compute, and what could still make the forecast wrong: the bootstrap covers parameter noise only, and in repeated simulations of this very design it covers the held-out run less often than its nominal 95 percent.

:::exercise{ref=capstone}
:::

## When you finish

You can fit a nonlinear law robustly, say how far its forecasts can be trusted, and recognize the two ways they fail without warning. L11 applies the machinery to real training runs; M38 starts from such forecasts.

:::edge{to=L11 text="scaling laws fitted to training runs."}
:::

:::edge{to=M38 text="forecasts that frontier training runs are planned on."}
:::
