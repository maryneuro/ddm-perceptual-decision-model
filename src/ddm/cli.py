from __future__ import annotations

import argparse

from ddm.config import DDMConfig
from ddm.plotting import save_decision_time_histogram
from ddm.simulation import simulate_ddm


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Drift Diffusion Model simulator")
    parser.add_argument("--n-trials", type=int, default=500)
    parser.add_argument("--drift", type=float, default=0.3)
    parser.add_argument("--noise", type=float, default=1.0)
    parser.add_argument("--dt", type=float, default=0.01)
    parser.add_argument("--boundary", type=float, default=1.0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--bins", type=int, default=30)
    parser.add_argument("--output", type=str, default="decision_time_distribution.png")
    parser.add_argument("--show-plot", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    config = DDMConfig(
        n_trials=args.n_trials,
        drift=args.drift,
        noise=args.noise,
        dt=args.dt,
        boundary=args.boundary,
        seed=args.seed,
        bins=args.bins,
        output_path=args.output,
        show_plot=args.show_plot,
    )
    decision_times, _ = simulate_ddm(config)
    save_decision_time_histogram(
        decision_times,
        bins=config.bins,
        output_path=config.output_path,
        show_plot=config.show_plot,
    )


if __name__ == "__main__":
    main()
