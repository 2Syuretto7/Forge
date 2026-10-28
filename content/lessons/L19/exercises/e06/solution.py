import copy
import numpy as np

TRUE_W = np.array([1.0, -2.0, 0.5])


def batch(rng, n=16):
    """A regression batch drawn from the trainer's generator."""
    X = rng.normal(size=(n, 3))
    return X, X @ TRUE_W + 0.1 * rng.normal(size=n)


def loss_grad(w, X, y):
    """0.5 * mean((X w - y)^2) and its gradient."""
    r = X @ w - y
    return 0.5 * np.mean(r ** 2), X.T @ r / len(y)


def new_state(seed):
    """Everything a run carries: weights, Adam moments and step, and the data generator."""
    return {"w": np.zeros(3), "m": np.zeros(3), "v": np.zeros(3), "step": 0, "rng": np.random.default_rng(seed)}


def train_steps(state, n, lr=0.05):
    """Run n Adam steps on fresh batches from state["rng"], updating state in place."""
    for _ in range(n):
        X, y = batch(state["rng"])
        _, g = loss_grad(state["w"], X, y)
        state["step"] += 1
        state["m"] = 0.9 * state["m"] + 0.1 * g
        state["v"] = 0.999 * state["v"] + 0.001 * g * g
        mh = state["m"] / (1 - 0.9 ** state["step"])
        vh = state["v"] / (1 - 0.999 ** state["step"])
        state["w"] = state["w"] - lr * mh / (np.sqrt(vh) + 1e-8)
    return state


def save(state):
    """A checkpoint that shares nothing with the live state: copies of the arrays, the step and the
    generator's bit_generator.state."""
    return {"w": state["w"].copy(), "m": state["m"].copy(), "v": state["v"].copy(), "step": state["step"],
            "rng": copy.deepcopy(state["rng"].bit_generator.state)}


def load(ckpt):
    """A live state from a checkpoint."""
    rng = np.random.default_rng()
    rng.bit_generator.state = copy.deepcopy(ckpt["rng"])
    return {"w": ckpt["w"].copy(), "m": ckpt["m"].copy(), "v": ckpt["v"].copy(), "step": ckpt["step"], "rng": rng}
