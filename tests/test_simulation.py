import numpy as np

from ddm.config import DDMConfig
from ddm.simulation import simulate_ddm


def test_simulate_ddm_shapes_and_domain() -> None:
    config = DDMConfig(n_trials=50, seed=7)
    decision_times, choices = simulate_ddm(config)

    assert decision_times.shape == (50,)
    assert choices.shape == (50,)
    assert np.all(decision_times > 0)
    assert np.all(np.isin(choices, [0, 1]))


def test_simulate_ddm_is_reproducible_with_fixed_seed() -> None:
    config = DDMConfig(n_trials=25, seed=123)

    dt1, ch1 = simulate_ddm(config)
    dt2, ch2 = simulate_ddm(config)

    assert np.array_equal(dt1, dt2)
    assert np.array_equal(ch1, ch2)


def test_simulate_ddm_variation_changes_with_drift() -> None:
    low = DDMConfig(n_trials=500, drift=0.1, seed=42)
    high = DDMConfig(n_trials=500, drift=0.6, seed=42)

    low_dt, _ = simulate_ddm(low)
    high_dt, _ = simulate_ddm(high)

    assert high_dt.mean() < low_dt.mean()
