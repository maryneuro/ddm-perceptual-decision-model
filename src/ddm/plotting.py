from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def save_decision_time_histogram(
    decision_times: np.ndarray,
    bins: int,
    output_path: str,
    show_plot: bool = False,
) -> None:
    """Save (and optionally display) a histogram of decision times."""
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    plt.figure()
    plt.hist(decision_times, bins=bins)
    plt.xlabel("Decision Time (s)")
    plt.ylabel("Frequency")
    plt.title("Simulated Decision Time Distribution")
    plt.tight_layout()
    plt.savefig(output)

    if show_plot:
        plt.show()

    plt.close()
