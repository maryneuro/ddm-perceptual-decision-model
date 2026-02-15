from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DDMConfig:
    """Configuration for a drift diffusion simulation."""

    n_trials: int = 500
    drift: float = 0.3
    noise: float = 1.0
    dt: float = 0.01
    boundary: float = 1.0
    seed: int | None = 42
    bins: int = 30
    output_path: str = "decision_time_distribution.png"
    show_plot: bool = False

    def validate(self) -> None:
        """Validate simulation and plotting parameters."""
        if self.n_trials <= 0:
            raise ValueError("n_trials must be > 0")
        if self.noise < 0:
            raise ValueError("noise must be >= 0")
        if self.dt <= 0:
            raise ValueError("dt must be > 0")
        if self.boundary <= 0:
            raise ValueError("boundary must be > 0")
        if self.bins <= 0:
            raise ValueError("bins must be > 0")
