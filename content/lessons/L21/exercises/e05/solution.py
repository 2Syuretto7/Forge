import numpy as np


def ppo_objective(logp, logp_old, adv, eps):
    """The mean over samples of min(rho A, clip(rho, 1 - eps, 1 + eps) A) with rho = exp(logp -
    logp_old), and its gradient with respect to logp (zero where the clipped term is the smaller)."""
    rho = np.exp(logp - logp_old)
    unclipped = rho * adv
    clipped = np.clip(rho, 1 - eps, 1 + eps) * adv
    use = unclipped <= clipped
    obj = np.mean(np.where(use, unclipped, clipped))
    grad = np.where(use, rho * adv, 0.0) / len(adv)
    return float(obj), grad
