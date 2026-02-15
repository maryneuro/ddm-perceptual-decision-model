from __future__ import annotations

import numpy as np

from ddm.config import DDMConfig


def simulate_ddm(config: DDMConfig) -> tuple[np.ndarray, np.ndarray]:
    """Run a drift diffusion simulation.

    Returns:
        Tuple of (decision_times, choices).
    """
    config.validate()
    rng = np.random.default_rng(config.seed)

    decision_times = np.empty(config.n_trials, dtype=float)
    choices = np.empty(config.n_trials, dtype=np.int8)

    for i in range(config.n_trials):
        evidence = 0.0
        elapsed = 0.0
        while abs(evidence) < config.boundary:
            evidence += config.drift * config.dt + config.noise * np.sqrt(config.dt) * rng.normal()
            elapsed += config.dt

        decision_times[i] = elapsed
        choices[i] = 1 if evidence > 0 else 0

    return decision_times, choices
