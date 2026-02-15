import pytest

from ddm.config import DDMConfig


@pytest.mark.parametrize(
    "kwargs",
    [
        {"n_trials": 0},
        {"noise": -1.0},
        {"dt": 0.0},
        {"boundary": 0.0},
        {"bins": 0},
    ],
)
def test_config_validation_rejects_invalid_values(kwargs: dict[str, float | int]) -> None:
    config = DDMConfig(**kwargs)
    with pytest.raises(ValueError):
        config.validate()


def test_config_validation_accepts_defaults() -> None:
    DDMConfig().validate()
