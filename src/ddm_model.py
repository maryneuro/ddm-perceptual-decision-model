import os
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

THRESHOLD = 1.0
DT = 0.01


def simulate_ddm(n_trials=500, drift=0.3, noise=1.0, threshold=THRESHOLD, dt=DT):
    """Simulate a basic DDM with absorbing boundaries at ±threshold."""
    decision_times = np.empty(n_trials, dtype=float)
    choices = np.empty(n_trials, dtype=int)

    for i in range(n_trials):
        evidence = 0.0
        t = 0.0
        while abs(evidence) < threshold:
            evidence += drift * dt + noise * np.sqrt(dt) * np.random.randn()
            t += dt

        decision_times[i] = t
        choices[i] = 1 if evidence > 0 else 0

    return decision_times, choices


def summary_stats(decision_times, choices):
    """Compute simple summary stats for fitting."""
    acc = choices.mean()                 # P(choice=1)
    mrt = decision_times.mean()          # mean RT
    srt = decision_times.std(ddof=1)     # std RT
    return acc, mrt, srt


def fit_drift_gridsearch(obs_dt, obs_ch, noise=1.0, threshold=THRESHOLD, dt=DT,
                         drift_grid=None, n_sim=800, w_acc=1.0, w_mrt=1.0):
    """
    Fit drift via crude grid search by matching accuracy + mean RT.
    This is intentionally simple but demonstrates parameter estimation.
    """
    if drift_grid is None:
        drift_grid = np.linspace(-0.8, 0.8, 33)

    obs_acc, obs_mrt, _ = summary_stats(obs_dt, obs_ch)

    best = {"drift": None, "loss": np.inf, "pred_acc": None, "pred_mrt": None}

    for d in drift_grid:
        sim_dt, sim_ch = simulate_ddm(n_trials=n_sim, drift=d, noise=noise, threshold=threshold, dt=dt)
        pred_acc, pred_mrt, _ = summary_stats(sim_dt, sim_ch)

        # Simple weighted squared error on summary statistics
        loss = w_acc * (pred_acc - obs_acc) ** 2 + w_mrt * (pred_mrt - obs_mrt) ** 2

        if loss < best["loss"]:
            best.update({"drift": d, "loss": loss, "pred_acc": pred_acc, "pred_mrt": pred_mrt})

    return best


def ensure_results_dir(path="results"):
    os.makedirs(path, exist_ok=True)


def plot_rt_histogram(decision_times, out_path):
    plt.figure()
    plt.hist(decision_times, bins=30)
    plt.xlabel("Decision Time (s)")
    plt.ylabel("Frequency")
    plt.title("Simulated Decision Time Distribution")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()


def plot_fit_overlay(obs_dt, sim_dt, out_path):
    plt.figure()
    plt.hist(obs_dt, bins=30, alpha=0.6, label="Observed (simulated data)")
    plt.hist(sim_dt, bins=30, alpha=0.6, label="Best-fit DDM (resimulated)")
    plt.xlabel("Decision Time (s)")
    plt.ylabel("Frequency")
    plt.title("RT Distribution: Data vs Best-fit Model")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()


def main():
    ensure_results_dir("results")

    # --- Step 1: generate "observed" data (ground truth) ---
    true_drift = 0.35
    noise = 1.0
    n_trials = 500

    obs_dt, obs_ch = simulate_ddm(n_trials=n_trials, drift=true_drift, noise=noise)

    # Save basic plot
    plot_rt_histogram(obs_dt, "results/decision_time_distribution.png")

    # --- Step 2: fit drift (simple) ---
    fit = fit_drift_gridsearch(obs_dt, obs_ch, noise=noise, n_sim=800)

    # --- Step 3: resimulate with fitted parameter & compare ---
    sim_dt, sim_ch = simulate_ddm(n_trials=n_trials, drift=fit["drift"], noise=noise)
    plot_fit_overlay(obs_dt, sim_dt, "results/fit_overlay.png")

    # Print a compact report
    obs_acc, obs_mrt, obs_srt = summary_stats(obs_dt, obs_ch)
    pred_acc, pred_mrt, pred_srt = summary_stats(sim_dt, sim_ch)

    report = f"""
DDM quick fit report
--------------------
True drift:        {true_drift:.3f}
Fitted drift:      {fit['drift']:.3f}
Loss:              {fit['loss']:.6f}

Observed  acc/mRT/sdRT: {obs_acc:.3f} / {obs_mrt:.3f} / {obs_srt:.3f}
Predicted acc/mRT/sdRT: {pred_acc:.3f} / {pred_mrt:.3f} / {pred_srt:.3f}
"""
    print(report)

    with open("results/fit_report.txt", "w", encoding="utf-8") as f:
        f.write(report.strip() + "\n")


if __name__ == "__main__":
    main()